# VULTURE SDR/IQ: complete architecture and operating guide

> **Purpose:** explain the SDR and IQ portions of VULTURE literally, accurately,
and operationally.
>
> **Scope:** receive-only SDR integration, canonical `.iq` files, Python
analysis, native C analysis, integrity, provenance, quality checks, testing,
and troubleshooting.
>
> **Safety boundary:** use only receivers, files, frequencies, and systems you
own or are explicitly authorized to analyze. This guide does not add
transmission, arbitrary scanning, network probing, device discovery, or emitter
attribution.

---

## 1. What this repository is

VULTURE is an analysis platform with two relevant implementation layers:

1. **Python** is the orchestration and analysis layer. It handles data loading,
   metadata, summaries, manifests, statistical analysis, spectral analysis,
   quality checks, and optional receive-only hardware integration.
2. **C** is the native analysis layer. It provides compact, dependency-light
   routines for loading and measuring IQ data, with explicit memory ownership
   and return values.

The two layers are not two different radio protocols. They are two consumers of
the same data contract. The important shared object is a complex baseband IQ
sample:

```text
sample = I + jQ
```

`I` is the in-phase component. `Q` is the quadrature component. A sequence of
these samples represents a time-ordered recording of a receiver's baseband
output.

The sample values alone are not the complete measurement. Interpretation also
depends on sample rate, center frequency, gain, channel, timestamp, device,
calibration, antenna path, and authorization/provenance records.

---

## 2. The canonical file contract

The canonical interchange format is a raw `.iq` file containing little-endian
IEEE-754 `complex64` samples. Each sample is eight bytes:

```text
bytes 0..3:  float32 I, little-endian
bytes 4..7:  float32 Q, little-endian
```

The file therefore has this logical layout:

```text
I0 Q0 I1 Q1 I2 Q2 ...
```

The file has no self-describing header. Its sibling sidecar provides metadata:

```text
capture.iq
capture.json
```

A minimal sidecar is:

```json
{
  "format": "complex64-le",
  "sample_rate": 1000000
}
```

The sidecar may contain additional authorized metadata such as:

- `center_frequency_hz`;
- `gain_db`;
- `channel`;
- `device`;
- `antenna`;
- `timestamp_utc`;
- `sample_count`;
- `calibration`;
- `authorization_reference`;
- `operator`;
- `driver` and binding versions;
- `software_version`;
- `sha256`.

The sidecar is metadata, not a substitute for the sample file. A report must
make clear which fields came from the sample stream and which came from the
operator or receiver configuration.

### 2.1 Why `complex64` is used

`complex64` stores two 32-bit floating-point components. It is a practical
balance between precision, storage, and interoperability. Python NumPy uses
`complex64`; the C reader consumes the same two-float representation and
promotes values into the repository's analysis structure.

A `.iq` file is not automatically a live radio connection. It is a recording.
A live SDR connection is a separate, explicit receive-only operation that
produces a recording or an in-memory stream.

### 2.2 File invariants

A valid canonical capture must satisfy all of these rules:

- the suffix is `.iq`;
- the file is non-empty;
- the byte size is divisible by eight;
- every I and Q value is finite;
- samples are one-dimensional and ordered;
- the sample rate is positive;
- the byte order is little-endian;
- the sidecar and capture refer to the same recording;
- any hash is calculated over the exact file being reported.

Malformed, truncated, empty, NaN, and infinite captures must fail closed.

---

## 3. Python file boundary

The Python shared boundary is implemented in:

```text
src/vulture/sdr_iq_framework/partition.py
```

The principal operations are:

- `read_iq_file(path, sample_rate=None)`;
- `write_iq_file(path, samples, sample_rate)`;
- `IQFileError` for malformed input.

`read_iq_file` accepts the canonical `.iq` path and reads the optional JSON
sidecar. The explicit `sample_rate` argument takes precedence over sidecar
metadata. The reader validates shape, complexity, non-empty data, finite
values, and sample rate.

`write_iq_file` accepts complex samples, validates them, writes little-endian
complex64 bytes, and writes the sidecar. It does not invent center frequency,
device identity, calibration, or hardware provenance.

Example:

```python
from pathlib import Path
import numpy as np

from vulture.sdr_iq_framework.partition import read_iq_file, write_iq_file

samples = np.asarray([1 + 0j, 0 + 1j, -1 + 0j], dtype=np.complex64)
write_iq_file(Path("capture.iq"), samples, sample_rate=1_000_000)
loaded, rate = read_iq_file("capture.iq")
assert loaded.dtype == np.complex64
assert rate == 1_000_000
```

This operation is file canonicalization. It is not a conversion from a
simulation into a physical observation.

---

## 4. Python receive-only boundary

The receive-only boundary is represented by `ReceiveConfig` and
`ReceiveOnlySource` in the RF-DNA adapter. A configuration contains:

```python
from vulture.rf_dna.cli import ReceiveConfig, ReceiveOnlySource

config = ReceiveConfig(
    sample_rate=1_000_000,
    center_frequency=100_000_000,
    gain=None,
    device_args="driver=approved-device",
)
source = ReceiveOnlySource(config)
```

The validation rules are intentionally conservative:

- sample rate must be greater than zero;
- center frequency must not be negative;
- device arguments must be explicit before opening hardware;
- the optional SoapySDR binding must be installed;
- the caller must provide an approved device configuration;
- only the receive direction is used;
- no transmit stream is created;
- no device discovery is performed by the adapter.

A hardware stream is opened only by an explicit call such as:

```python
device, stream = source.open_soapysdr()
```

That call is environment-dependent and cannot be verified merely by importing
VULTURE. A successful import of SoapySDR does not prove that a receiver is
connected, authorized, tuned correctly, calibrated, or safe to use.

A production capture loop should always release the stream in a `finally` block
or context manager. It should also bound the sample count and chunk size so a
configuration mistake cannot allocate unbounded memory.

---

## 5. Capture manifests: the smart summary layer

The smart summary layer is:

```text
src/vulture/sdr_iq_framework/capture_manifest.py
```

It has two important concepts:

1. **Summary:** calculate facts about a capture and return JSON-compatible
   values.
2. **Canonicalization:** copy an existing recording into canonical `.iq` form
   and write a manifest beside it.

The manifest records facts such as:

- format;
- source label;
- hardware verification status;
- path;
- SHA-256;
- sample count;
- sample rate;
- duration;
- dtype;
- I and Q means;
- RMS;
- peak magnitude;
- mean power;
- software and Python version.

Example:

```python
from vulture.sdr_iq_framework.capture_manifest import (
    canonicalize_iq_capture,
    summarize_iq_capture,
)

summary = summarize_iq_capture(
    "capture.iq",
    source="recorded_iq",
    require_hardware=False,
)

canonicalize_iq_capture(
    "capture.iq",
    "canonical_capture.iq",
    source="sdr",
    require_hardware=True,
)
```

The `require_hardware` switch is a truthfulness gate. It does not inspect the
physical world and cannot prove hardware origin by itself. It prevents a caller
from labeling an explicitly synthetic source as hardware-verified. A genuine
lab workflow must supply and preserve its own authorization and acquisition
records.

A report should never say “real SDR” merely because a file has an `.iq` suffix.
The suffix proves format, not origin.

---

## 6. Integrity and provenance

Integrity answers: “Did these bytes change?” Provenance answers: “Where did the
bytes come from, under what configuration, and who recorded the context?”

The SHA-256 digest is calculated over the raw `.iq` bytes. It is useful for:

- detecting accidental modification;
- pairing a report with the exact input;
- comparing archived copies;
- recording chain-of-custody events;
- reproducibility.

It does **not** prove:

- transmitter identity;
- operator identity;
- location;
- intent;
- legality;
- calibration accuracy;
- uniqueness of origin.

Recommended capture record:

```json
{
  "capture": "capture.iq",
  "format": "complex64-le",
  "sha256": "...",
  "sample_rate_hz": 1000000,
  "center_frequency_hz": 100000000,
  "channel": 0,
  "device": "approved-receiver",
  "gain_db": null,
  "timestamp_utc": "2026-09-23T00:00:00Z",
  "authorization_reference": "LAB-0001",
  "hardware_verified": true
}
```

Only include sensitive device, location, or operator fields when policy permits.

---

## 7. Python analysis features

The Python SDR/IQ framework contains focused modules rather than one opaque
function. The main analysis surfaces are:

### 7.1 Integrity

`integrity.py` calculates file hashes and checks complete complex64 sample
boundaries. A file with a partial final sample is rejected.

### 7.2 Statistics

`statistics.py` calculates descriptive values:

- sample count;
- mean I;
- mean Q;
- RMS magnitude;
- peak magnitude;
- mean power;
- crest factor.

These describe the supplied capture. They do not identify a device.

### 7.3 Spectral analysis

`spectral.py` calculates a centered FFT frequency axis and power spectrum. The
frequency axis is only meaningful when the sample rate is correct. Window choice
changes leakage and resolution and must be recorded.

The current helper supports a Hann or rectangular window. An occupied-bandwidth
estimate is a threshold/model result, not a universal physical bandwidth
measurement.

### 7.4 Quality checks

`quality.py` checks:

- one-dimensional shape;
- non-empty data;
- finite I/Q values;
- complex dtype;
- positive sample rate;
- fraction of samples at or beyond a nominal unit clipping threshold.

Clipping interpretation depends on the receiver's scale and calibration. The
quality report must not present the nominal threshold as a universal ADC limit.

### 7.5 Bounded streaming

`stream.py` provides bounded chunk iteration for large `.iq` files. Reading in
chunks avoids loading an arbitrarily large capture into memory. A streaming
analysis should aggregate state rather than concatenate every chunk.

### 7.6 Receive stream lifecycle

The stream helper wraps activation and cleanup. Cleanup is essential because a
left-open hardware stream can retain the device, lose samples, or interfere
with later authorized captures.

### 7.7 JSON-ready commands

`commands.py` combines manifest, integrity, statistics, quality, and occupied
bandwidth into a single inspection result. It is an analysis operation over an
existing `.iq` capture; it is not a radio-control operation.

---

## 8. Native C layer

The C layer uses the repository's IQ structures and explicit cleanup rules.
The reader consumes the same little-endian complex64 pair layout as Python.
C values may be represented internally as two `double` fields for numerical
analysis, while the file representation remains two float32 values per sample.

The essential ownership pattern is:

```c
VultureIQBuffer buffer = {0};
if (vulture_iq_read_complex64_le("capture.iq", &buffer) != 0) {
    /* report an input error */
}
/* analyze buffer */
vulture_iq_free(&buffer);
```

Every successful allocation must have one clear release path. Error paths must
release partially allocated memory before returning.

The C feature modules are intentionally small and reviewable. They cover:

- sample loading;
- mean power and RMS;
- peak and crest factor;
- DC I and DC Q;
- phase mean and variance;
- I/Q correlation and gain imbalance;
- zero-crossing and frequency estimate;
- strict finite-value validation.

These functions are descriptive. They do not open hardware, transmit, scan,
contact a network, or infer a transmitter identity.

### 8.1 C compilation expectations

The native code is C11 and uses strict warnings:

```bash
make -C c clean
make -C c
```

For a focused compiler check:

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic -O2 -I c \
  -c c/vulture_iq_partition.c -o /tmp/vulture_iq_partition.o
```

For sanitizers where supported:

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic -g \
  -fsanitize=address,undefined -I c \
  -c c/vulture_iq_partition.c -o /tmp/vulture_iq_partition_sanitized.o
```

A successful compile is not numerical validation. Run functional tests with
known captures and compare C and Python summaries within an explicitly chosen
tolerance.

### 8.2 C and Python agreement test

A cross-language verification should use one fixed `.iq` file and compare:

- sample count;
- mean I and Q;
- RMS;
- peak;
- power;
- phase statistics;
- frequency estimate where the algorithms are intentionally equivalent.

If implementations use different windows or estimators, the report must state
that the values are not expected to match exactly.

---

## 9. Commands and command design

Commands should be explicit about input, metadata, and output. A good command
never silently changes a file's provenance.

### 9.1 Python package installation

```bash
python -m pip install -e .
python -m pip install -e ".[dev]"
```

### 9.2 Python tests

```bash
pytest -q
pytest -q tests/test_sdr_iq_contract.py
pytest -q tests/test_capture_manifest.py
```

Use the repository's actual CLI help to discover currently wired commands:

```bash
vulture --help
vulture rf-dna --help
python -m vulture.rf_dna.cli --help
```

Do not assume a module exists as a CLI command merely because a helper function
exists. If a command is not wired in Click, invoke the Python API or add an
explicit command wrapper and tests.

### 9.3 C build and existing binaries

```bash
make -C c
./vulture_cli --help
./vulture-c --help
```

The exact executable list is controlled by `c/Makefile`. New object files must
be added to a target or a library; placing a `.c` file in the directory does not
compile or expose it automatically.

### 9.4 File inspection workflow

```bash
sha256sum capture.iq
python -m json.tool capture.json
```

Python API example:

```bash
python - <<'PY'
from vulture.sdr_iq_framework.commands import inspect_capture
import json
print(json.dumps(inspect_capture("capture.iq"), indent=2))
PY
```

This requires the capture sidecar to contain a valid positive sample rate.

### 9.5 Hardware capture workflow

A hardware workflow must be configured for an approved receiver. The generic
sequence is:

1. verify authorization;
2. install the receiver's supported driver/binding;
3. choose a legal and approved center frequency;
4. set a positive sample rate;
5. set gain explicitly or use a documented automatic mode;
6. provide explicit device arguments;
7. open RX only;
8. capture a bounded number of samples;
9. close the stream in all paths;
10. write `.iq` plus sidecar metadata;
11. hash the capture;
12. analyze locally;
13. preserve the command/configuration and software revision.

There is no generic universal device string. The device arguments are
vendor- and environment-specific and must not be guessed.

---

## 10. What “real” means here

There are three distinct meanings that must not be conflated:

### 10.1 Real file format

A file is real in the format sense when it conforms to the `.iq` byte contract.
A program can verify this mechanically.

### 10.2 Real recorded data

A file is recorded data when it was written from an actual acquisition or an
existing recording. The software cannot prove this from bytes alone. It needs
trusted acquisition metadata and process records.

### 10.3 Real-world measurement

A measurement claim depends on receiver calibration, antenna path, sample-rate
accuracy, gain, frequency reference, clock stability, environmental conditions,
and a documented procedure. VULTURE can preserve those claims as metadata; it
cannot manufacture them after the fact.

For that reason, the project must never provide a function that silently
“converts” simulated samples into real SDR evidence. It may convert formats,
but it must preserve the source label and reject false hardware certification.

---

## 11. Purple-team and defensive use

SDR/IQ analysis can support defensive engineering without becoming an
operational control system. Appropriate defensive uses include:

- validating capture integrity;
- detecting truncation and malformed samples;
- detecting unexpected clipping;
- comparing authorized recordings for repeatability;
- identifying configuration drift;
- checking whether sample rates and center frequencies agree;
- recording driver and software versions;
- reviewing anomalies in a controlled lab;
- testing parser resilience with malformed files;
- validating memory bounds and cleanup;
- comparing Python and C implementations;
- auditing that transmit paths are absent or disabled.

Results should be expressed as observations: “the capture contains X samples,”
“the mean I is Y,” or “the file hash differs.” Avoid unsupported statements
such as “this proves device Z transmitted the signal.”

---

## 12. Testing strategy

Testing should proceed from the file contract outward.

### 12.1 Unit tests

Unit tests should cover:

- valid complex64 round trips;
- sidecar sample-rate loading;
- explicit sample-rate override;
- empty files;
- truncated files;
- real-valued arrays;
- multidimensional arrays;
- NaN and infinite values;
- negative and zero sample rates;
- non-complex input;
- deterministic SHA-256 values;
- statistics on known samples;
- quality reports for clipped and unclipped values;
- spectrum rejection for too-short inputs;
- bounded chunk iteration;
- manifest rejection of synthetic provenance when hardware is required.

### 12.2 Integration tests

Integration tests should verify:

- Python writes a file that C reads;
- C writes or consumes the same byte order expected by Python;
- both sides reject malformed data;
- cleanup occurs after read errors;
- manifest hashes match the exact capture;
- reports include the sidecar sample rate;
- hardware tests are opt-in and skipped without explicit lab configuration.

### 12.3 Property tests

Useful properties include:

- writing then reading preserves samples within float32 representation;
- appending complete samples preserves byte divisibility by eight;
- changing one byte changes the SHA-256 digest;
- scaling samples scales RMS and peak predictably;
- replacing Q with `-Q` changes phase orientation but preserves magnitude;
- a zero signal has zero power and a non-error zero crest factor policy;
- non-finite input is always rejected.

### 12.4 Native memory tests

Compile C with AddressSanitizer and UndefinedBehaviorSanitizer. Exercise:

- missing files;
- empty files;
- truncated final pairs;
- allocation growth;
- non-finite samples;
- repeated free;
- error after partial allocation;
- large but bounded captures.

The test goal is not merely “no crash.” It is clear ownership, bounded input,
correct return codes, and no use-after-free or integer overflow.

### 12.5 Hardware tests

Hardware tests require an explicitly authorized lab and should be marked with a
hardware test marker. They should never run automatically in ordinary CI.
They must have:

- a known receiver;
- a known driver/binding;
- a controlled frequency and sample rate;
- a bounded capture duration;
- a cleanup fixture;
- no transmission path;
- no arbitrary scanning;
- local-only result storage.

---

## 13. Troubleshooting

### “Sample rate is missing”

Provide a positive sample rate argument or create the matching JSON sidecar.
Do not guess a default for a measurement report. A wrong sample rate produces a
wrong time and frequency axis.

### “The `.iq` file is empty”

Check the capture loop, output path, permissions, and whether the SDR returned
samples. Do not replace an empty capture with synthetic data and call it a
successful acquisition.

### “The byte count is invalid”

A canonical complex64 capture must be divisible by eight. The file may have
been truncated or written with a different sample format. Identify the actual
format before converting it.

### “The spectrum looks wrong”

Check sample rate, center frequency, byte order, I/Q order, window, capture
length, clock reference, and whether the receiver used signed integer rather
than float samples.

### “Python and C differ”

Check dtype conversion, endianness, windowing, estimator definitions, phase
wrapping, sample-count limits, and whether one side includes a sidecar rate
while the other uses a command-line rate.

### “SoapySDR is unavailable”

Install the approved binding and vendor driver in the environment intended for
the receiver. The correct fallback is an existing `.iq` recording, not silent
device discovery and not a fabricated hardware result.

### “The receiver opens but samples are unusable”

Check channel index, gain, antenna path, clock, sample rate support, center
frequency support, permissions, and driver logs. Preserve the configuration in
the capture manifest.

### “Memory use is too high”

Use bounded chunk processing. Avoid concatenating every block. Set explicit
maximum sample counts and reject unreasonably large requests.

---

## 14. Review checklist

Before accepting an SDR/IQ change, reviewers should ask:

1. Does the change use the canonical `.iq` contract?
2. Is endianness explicit?
3. Are I and Q ordering documented?
4. Is sample rate required and validated?
5. Are empty and malformed inputs rejected?
6. Are NaN and infinity rejected?
7. Is source provenance preserved?
8. Can synthetic data be mistaken for hardware data?
9. Is `require_hardware` behavior truthful?
10. Is memory bounded?
11. Are all allocated buffers released?
12. Are receive and transmit directions clearly separated?
13. Is device configuration explicit?
14. Is network access absent?
15. Are reports descriptive rather than attribution claims?
16. Are C and Python definitions aligned?
17. Are new C files included in the build graph?
18. Are commands wired and tested?
19. Are hardware tests opt-in?
20. Does documentation match the actual implementation?

A feature is not complete when it merely exists in a source file. It is
complete when it is wired, tested, documented, bounded, and honest about what
it can establish.

---

## 15. Practical end-to-end example

The following example assumes an authorized receiver has already produced
`receiver_capture.iq` and `receiver_capture.json`.

### Step 1: verify metadata

```bash
python -m json.tool receiver_capture.json
```

Confirm that `sample_rate` is positive and that the metadata corresponds to the
capture.

### Step 2: verify the file hash

```bash
sha256sum receiver_capture.iq
```

Record the output in the local evidence record.

### Step 3: inspect with Python

```bash
python - <<'PY'
import json
from vulture.sdr_iq_framework.commands import inspect_capture

result = inspect_capture("receiver_capture.iq")
print(json.dumps(result, indent=2))
PY
```

### Step 4: save a manifest

```bash
python - <<'PY'
from vulture.sdr_iq_framework.capture_manifest import summarize_iq_capture
import json

result = summarize_iq_capture("receiver_capture.iq", source="sdr")
with open("receiver_capture.manifest.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)
    f.write("\n")
PY
```

### Step 5: run Python tests

```bash
pytest -q tests/test_sdr_iq_contract.py tests/test_capture_manifest.py
```

### Step 6: build C

```bash
make -C c clean
make -C c
```

### Step 7: compare outputs

Use the same file, rate, sample range, and analysis definition in both layers.
Document any expected differences caused by numerical precision or distinct
algorithms.

### Step 8: archive the record

Keep the `.iq`, JSON sidecar, manifest, command/configuration, software commit,
hash, and authorization reference together according to local policy.

---

## 16. What this guide does not claim

This guide does not claim that:

- every SDR vendor is supported;
- SoapySDR is installed;
- a file's extension proves acquisition origin;
- statistical features identify a transmitter;
- a sample-rate field proves calibration;
- a C binary automatically connects to hardware;
- a Python import proves a receiver is present;
- a simulator output is a measurement;
- an analysis report is a legal conclusion;
- a hash proves authenticity without a trusted recording process.

The strength of the system comes from keeping these boundaries explicit. A
smaller truthful feature is more valuable than a larger feature that invents
hardware state, hides provenance, or turns a test fixture into a false claim.

---

## 17. Final operational summary

The complete mental model is:

```text
approved SDR or existing recording
              |
              v
        complex I/Q samples
              |
              v
        canonical .iq file
              +----> JSON metadata
              +----> SHA-256 integrity record
              |
              v
       Python and/or C reader
              |
              +----> validation
              +----> statistics
              +----> spectrum
              +----> quality checks
              +----> manifest
              |
              v
       descriptive local report
```

The arrows are deliberately one-way. Analysis does not become transmission.
Metadata does not become proof. A simulation does not become a real capture by
being renamed. A file conversion preserves samples and provenance; it does not
manufacture a physical event.

That is the original, strong, auditable SDR/IQ design: explicit inputs,
canonical bytes, bounded processing, receive-only hardware boundaries,
reviewable C and Python code, reproducible reports, and no claims beyond the
evidence supplied.
