# 🦅 VULTURE

## Scientific, RF, SDR/IQ, Forensics, and Research Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![C11](https://img.shields.io/badge/C11-native-00599C?logo=c&logoColor=white)](c/README.md)
[![RF-DNA](https://img.shields.io/badge/RF--DNA-receive--only-0A7B5E)](#rf-dna-and-sdriq)
[![License](https://img.shields.io/badge/License-AGPL--3.0-blue)](LICENSE)

VULTURE is a modular, offline-first platform for scientific calculation, RF and SDR/IQ analysis, chemistry, physics, mathematics, forensic review, signal processing, provenance, visualization, and reproducible research.

The repository contains a Python application layer and an optional native C layer. Python provides the primary CLI, orchestration, simulation, reporting, and extensibility. C provides compact, deterministic utilities for local numeric signals, file integrity, RF calculations, and IQ analysis.

> **Authorized use only.** Use VULTURE with data, receivers, frequencies, and systems that you own or are explicitly authorized to analyze.
>
> **Receive/analyze only.** VULTURE does not provide RF transmission, network probing, unauthorized monitoring, or automatic device discovery.

---

## Contents

1. [Project scope](#project-scope)
2. [Capabilities](#capabilities)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Linux distribution support](#linux-distribution-support)
6. [Quick start](#quick-start)
7. [Main CLI](#main-cli)
8. [RF and physics](#rf-and-physics)
9. [Chemical-RF](#chemical-rf)
10. [Forensic audits](#forensic-audits)
11. [RF-DNA and SDR/IQ](#rf-dna-and-sdriq)
12. [Using an SDR safely](#using-an-sdr-safely)
13. [SDR data formats](#sdr-data-formats)
14. [Signal-processing workflow](#signal-processing-workflow)
15. [Interactive shell](#interactive-shell)
16. [GUI](#gui)
17. [Offline analysis](#offline-analysis)
18. [Native C layer](#native-c-layer)
19. [C++ and C# boundaries](#c-and-c-boundaries)
20. [Reports and provenance](#reports-and-provenance)
21. [Testing](#testing)
22. [Sanitizers and native validation](#sanitizers-and-native-validation)
23. [Troubleshooting](#troubleshooting)
24. [Project structure](#project-structure)
25. [Limitations and responsible use](#limitations-and-responsible-use)
26. [Distribution references](#distribution-references)
27. [Roadmap](#roadmap)
28. [License](#license)

---

### Canonical native SDR/IQ command library

The C layer now has an additive `vulture-iq` command source at
`c/vulture_iq_cli.c`. It provides direct commands for the canonical IQ file
boundary:

```bash
./vulture-iq sdr status
./vulture-iq iq validate capture.iq
./vulture-iq iq stats capture.iq --sample-rate 1000000
```

These commands are receive/analyze-only. They read explicit `.iq` files and
never transmit, scan, discover devices, access networks, or open hardware
implicitly. The existing commands and files remain unchanged.

For the shared format, each `.iq` sample is a little-endian complex64 value:
`float32 I` followed by `float32 Q`. Use the Python partition writer to create
an authorized recording or convert an existing recording while preserving its
provenance:

```python
from vulture.sdr_iq_framework.partition import read_iq_file
samples, rate = read_iq_file("capture.iq")
```

The native command reports descriptive measurements only. A file extension,
hash, or statistical report does not prove transmitter identity, calibration,
location, authorization, or physical origin.


## Project scope

VULTURE is an analysis platform, not an autonomous radio-control platform. It is intended for:

- deterministic scientific calculations;
- local or prerecorded IQ analysis;
- authorized receive-only SDR workflows;
- simulator development without hardware;
- reproducible RF-DNA feature experiments;
- forensic review of supplied evidence;
- file hashing and provenance tracking;
- optional ML and visualization workflows;
- native C analysis where a compact binary is useful.

VULTURE separates calculation from collection. A local file can be analyzed without a receiver. A simulator can produce a repeatable fixture without a device. An optional receiver adapter is only relevant when the operator deliberately supplies a valid configuration and has authorization to use the device.

The repository documentation distinguishes three kinds of output:

1. **Calculation:** a mathematical result from supplied parameters.
2. **Analysis:** descriptive features calculated from supplied samples.
3. **Evidence or measurement:** a result whose interpretation depends on provenance, calibration, hardware, and human review.

The first two do not automatically become the third.

---

## Capabilities

### Scientific tools

- wavelength calculation;
- free-space path-loss calculation;
- NMR/Larmor-frequency calculation;
- complex-permittivity screening;
- dielectric resonance estimation;
- impedance reporting with explicit uncalibrated status;
- spectroscopy and local signal simulation;
- matrix, vector, protocol, and frame audits;
- uncertainty and provenance helpers.

### SDR and signal processing

- deterministic IQ simulation;
- NPZ capture loading;
- descriptive RF-DNA fingerprints;
- local dashboards and reports;
- FFT and DFT-oriented workflows;
- PSD, spectrogram, and waterfall workflows where the relevant modules are installed;
- peak, burst, occupancy, and noise-floor analysis;
- IQ metadata and provenance handling;
- optional receive-only adapter boundaries;
- local C IQ statistics and health checks.

### Evidence and review

- SHA-256 file and capture hashes;
- case and subject identifiers;
- JSON and text report formats;
- local audit metadata;
- explicit authorization and review fields;
- bounded input sizes;
- fail-closed validation.

### Optional research surfaces

- ML feature extraction and model evaluation;
- anomaly and time-series workflows;
- ONNX-related optional components;
- quantum-inspired comparisons with classical baselines;
- PyQt6 visualization and review surfaces.

---

## Architecture

### Python CLI

`src/vulture/cli.py` defines the primary Click application. It exposes status, information, RF calculations, the Chemical-RF route, RF-DNA commands, forensic commands, the lab group, and the interactive shell.

### Chemical-RF package

`src/vulture/chemical_rf/` contains scientific helpers and a dedicated command group. It covers material screening, NMR, physics, and impedance reporting.

### RF-DNA package

`src/vulture/rf_dna/` contains the simulator, local NPZ reader, fingerprinting, dashboards, reports, and optional receive-only boundaries.

### Offline tools

`src/vulture/offline_tools/` contains dependency-light local statistics, validation, DFT, provenance, windowing, and report helpers.

### C layer

`c/` is a separate native layer. It is not a replacement for the Python application and does not automatically connect to SDR hardware. See [Native C layer](#native-c-layer).

---

## Installation

### Python installation

```bash
git clone https://github.com/black-210/VULTURE.git
cd VULTURE
python -m pip install -e .
```

### Development installation

```bash
python -m pip install -e ".[dev]"
```

### Optional extras

```bash
python -m pip install -e ".[science]"
python -m pip install -e ".[ml]"
python -m pip install -e ".[security]"
python -m pip install -e ".[gui]"
```

The simulator and local-file workflows should work without optional SDR drivers. Optional hardware packages are environment-specific and must be installed according to the receiver vendor and laboratory policy.

### Verify installation

```bash
vulture --help
vulture info
vulture status
pytest -q
```

---

## Linux distribution support

VULTURE is documented for use in security-focused Linux ecosystems:

- **BlackArch Linux:** `vulture-black`
  <https://blackarch.org/radio.html>
- **Pentoo Linux:** `net-wireless/vulture`
  <https://github.com/pentoo/pentoo-overlay>

These references describe package ecosystems; they do not change VULTURE’s receive-only design. Review package contents, permissions, licenses, device behavior, and local legal requirements before installation.

---

## Quick start

```bash
vulture info
vulture status
vulture rf-wavelength --frequency-hz 1000000000
vulture rf-path-loss --frequency-hz 2400000000 --distance-m 10
vulture chemical-rf nmr --nucleus 1H --field-t 7
vulture rf-dna status
vulture --interactive
```

Expected status fields include:

```json
{
  "analysis": "local-only",
  "hardware": "not-opened",
  "mode": "offline-deterministic",
  "network": "disabled",
  "rf_transmit": "disabled"
}
```

---

## Main CLI

List the main command help:

```bash
vulture --help
```

### Information

```bash
vulture info
```

### Runtime safety status

```bash
vulture status
```

### Interactive mode

```bash
vulture --interactive
```

The main CLI validates arguments with Click, invokes local functions, and prints JSON or text. It does not open hardware merely because the CLI is installed.

---

## RF and physics

### Wavelength

```bash
vulture rf-wavelength --frequency-hz 1000000000
```

The command returns the supplied frequency and calculated wavelength in metres.

### Free-space path loss

```bash
vulture rf-path-loss \
  --frequency-hz 2400000000 \
  --distance-m 10
```

This uses supplied frequency and distance. It is not a live link measurement and does not account for every antenna, environment, cable, or propagation effect.

### Native RF calculation

```bash
make -C c
./vulture_rf_analysis 2400000000 10
```

---

## Chemical-RF

Show commands:

```bash
vulture chemical-rf --help
```

The project also provides the standalone entry point:

```bash
vulture-chemical-rf --help
```

### NMR

```bash
vulture chemical-rf nmr --nucleus 1H --field-t 7
```

### Material screening

```bash
vulture chemical-rf material \
  --epsilon-r 4.2 \
  --conductivity 0.01 \
  --frequency-hz 2400000000 \
  --length-m 0.1
```

### Physics

```bash
vulture chemical-rf physics \
  --frequency-hz 2400000000 \
  --distance-m 10
```

### Impedance report

```bash
vulture chemical-rf report \
  --sample-id S-001 \
  --real-ohm 50 \
  --imag-ohm 2.5 \
  --frequency-hz 2400000000
```

The report is explicitly uncalibrated. Treat it as a structured analytical result, not a calibration certificate.

---

## Forensic audits

Forensic commands operate on supplied values and metadata.

### Physics

```bash
vulture forensic physics \
  --case-id C-001 \
  --subject capture \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --format json
```

To save a report:

```bash
vulture forensic physics \
  --case-id C-001 \
  --subject capture \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --format json \
  --output report.json
```

### Chemistry

```bash
vulture forensic chemistry \
  --case-id C-002 \
  --subject sample \
  --compounds-json '[{"elements":{"H":2,"O":1}}]'
```

### Mathematics

```bash
vulture forensic math \
  --case-id C-003 \
  --subject system \
  --matrix-json '[[2,1],[1,1]]' \
  --vector-json '[3,2]'
```

### Protocol/frame metadata

```bash
vulture forensic protocol \
  --case-id C-004 \
  --subject frame \
  --frames-json '[{"length":4,"declared_length":5}]'
```

Findings describe supplied input. They do not establish legal conclusions, attribution, identity, or intent by themselves.

---

# RF-DNA and SDR/IQ

This section describes the complete SDR-related workflow. VULTURE supports local simulation and local-file analysis first. Hardware integration is optional, explicit, receive-only, and environment-dependent.

## SDR terminology

### SDR

A software-defined radio uses software to process digitized radio samples. The receiver hardware normally provides complex baseband samples, represented as I/Q values.

### IQ samples

An IQ sample has two components:

- **I:** in-phase component;
- **Q:** quadrature component.

Together they form a complex sample:

```text
sample = I + jQ
```

A capture normally also needs metadata such as:

- sample rate;
- center frequency;
- timestamp or capture time;
- gain configuration;
- antenna or channel information;
- sample format;
- calibration status;
- source and authorization metadata.

Without metadata, an IQ file may still be processed, but interpretation is weaker.

### Sample rate

The sample rate describes how many complex samples are acquired per second. It determines the representable bandwidth and frequency scale for FFT or spectrogram output. A wrong sample rate produces a wrong frequency axis even if the sample values are valid.

### Center frequency

The center frequency identifies the RF frequency represented at baseband zero. The local simulator and report pipeline can preserve this metadata, but a file-analysis command cannot recover it if it was never recorded.

### Baseband

IQ processing generally operates on a complex baseband representation. A positive or negative frequency offset in the baseband corresponds to a frequency relative to the capture center frequency.

### Receive-only

A receive-only workflow reads or receives samples and analyzes them. It does not transmit, replay over RF, tune through arbitrary bands, discover devices, or probe networks.

---

## SDR workflow overview

A disciplined SDR workflow has these phases:

1. **Authorization:** confirm the device, frequency, location, and data are authorized.
2. **Environment preparation:** install approved drivers and verify permissions.
3. **Capability check:** run `vulture rf-dna backends`.
4. **Fixture validation:** test the simulator first.
5. **Capture or load:** use a local NPZ capture or an explicitly configured receive source.
6. **Metadata review:** record sample rate, center frequency, format, gain, and time.
7. **Signal analysis:** fingerprint, dashboard, report, or run downstream processing.
8. **Integrity recording:** hash the capture and save the command line and software version.
9. **Human review:** interpret results in context and avoid unsupported conclusions.

The normal path does not require hardware:

```bash
vulture rf-dna simulate \
  --profile multi-tone \
  --duration 1 \
  --sample-rate 1000000 \
  --seed 7 \
  --output fixture.npz

vulture rf-dna fingerprint \
  --input fixture.npz \
  --label local-fixture

vulture rf-dna dashboard \
  --input fixture.npz \
  --label local-fixture

vulture rf-dna report \
  --input fixture.npz \
  --label local-fixture
```

---

## Simulator profiles

The simulator is the safest first step because it requires no receiver.

### Noise

```bash
vulture rf-dna simulate \
  --profile noise \
  --duration 1 \
  --sample-rate 1000000 \
  --seed 7 \
  --output noise.npz
```

Noise fixtures are useful for baseline behavior, noise-floor tests, and checking that a downstream feature does not report structure where none was simulated.

### Multi-tone

```bash
vulture rf-dna simulate \
  --profile multi-tone \
  --duration 1 \
  --sample-rate 1000000 \
  --seed 7 \
  --output tones.npz
```

Multi-tone fixtures are useful for checking peak and frequency features.

### CW

```bash
vulture rf-dna simulate \
  --profile cw \
  --duration 1 \
  --sample-rate 1000000 \
  --seed 7 \
  --output cw.npz
```

### Chirp

```bash
vulture rf-dna simulate \
  --profile chirp \
  --duration 1 \
  --sample-rate 1000000 \
  --seed 7 \
  --output chirp.npz
```

### Reproducibility

Use the same profile, duration, sample rate, and seed to reproduce a fixture. Save those parameters with the resulting report.

---

## Checking SDR availability

Run:

```bash
vulture rf-dna status
vulture rf-dna backends
```

The backend report distinguishes:

- whether local NPZ analysis is available;
- whether the simulator is available;
- whether optional SoapySDR bindings are installed;
- whether transmission is supported by the VULTURE workflow;
- whether network probing is enabled.

The expected safety fields are:

```json
{
  "transmit": false,
  "network_probe": false,
  "local_npz": true,
  "simulator": true
}
```

An installed binding does not mean a device has been opened. Hardware access remains explicit and configuration-dependent.

---

## Connecting an approved SDR

VULTURE’s receive adapter is intentionally conservative. A generic command in this README must not pretend that every SDR, operating system, driver, and vendor API has the same connection procedure.

Use this process:

1. Connect only an approved receiver that you are authorized to use.
2. Install the vendor’s supported driver or SoapySDR binding according to its documentation.
3. Configure sample rate, center frequency, gain, and device arguments explicitly.
4. Confirm the device is receive-only for the planned workflow.
5. Run the backend status command.
6. Use the adapter through the repository’s supported Python API or lab-specific integration.
7. Save metadata and review output locally.

The adapter configuration concept is represented by fields like:

```python
from vulture.rf_dna.sdr_adapter import ReceiveConfig, ReceiveOnlySource

config = ReceiveConfig(
    sample_rate=1_000_000,
    center_frequency=100_000_000,
    gain=None,
    device_args="driver=approved-device",
)
source = ReceiveOnlySource(config)
```

This configuration is descriptive and must be adapted to the actual approved hardware and installed binding. It does not automatically discover a device.

When a local NPZ capture is available, prefer it for testing:

```python
from vulture.rf_dna.sdr_adapter import ReceiveOnlySource

iq, sample_rate = ReceiveOnlySource.from_npz("capture.npz")
```

For an explicitly configured receiver, the adapter boundary can be opened only after checking the installed backend and device arguments:

```python
source = ReceiveOnlySource(config)
device, stream = source.open_soapysdr()
```

The repository’s adapter intentionally requires explicit `device_args`. If the binding is unavailable, it fails with an offline-mode error instead of silently searching for hardware.

Do not interpret the example as permission to connect to unknown receivers. Use an approved device, an approved frequency plan, and local authorization.

---

## What to record for a hardware capture

For each authorized capture, preserve:

- operator and authorization reference;
- device model and serial identifier where policy permits;
- driver and binding versions;
- center frequency;
- sample rate;
- gain and antenna path;
- channel index;
- timestamp and time source;
- sample format;
- number of samples;
- calibration state;
- location metadata only when appropriate and authorized;
- file hash;
- command line or configuration;
- analysis software version.

A capture without metadata can still be useful for waveform processing, but it is harder to interpret and reproduce.

---

## Local NPZ capture format

The RF-DNA local loader expects an NPZ file containing:

- `iq`: a non-empty complex array;
- `sample_rate`: a positive number.

The simulator writes these fields and also records a source label. Example creation from Python:

```python
import numpy as np

samples = np.asarray([1 + 0j, 0 + 1j, -1 + 0j], dtype=np.complex64)
np.savez_compressed(
    "capture.npz",
    iq=samples,
    sample_rate=1_000_000.0,
    source="local-fixture",
)
```

Load it:

```python
from vulture.rf_dna.sdr_adapter import ReceiveOnlySource

iq, rate = ReceiveOnlySource.from_npz("capture.npz")
print(iq.shape, rate)
```

The loader rejects an absent `iq` array, empty data, and non-positive sample rates.

---

## Capture analysis commands

### Fingerprint

```bash
vulture rf-dna fingerprint \
  --input capture.npz \
  --label approved-capture
```

This extracts a descriptive fingerprint from local samples. The label is an operator-provided label, not a verified identity.

### Dashboard

```bash
vulture rf-dna dashboard \
  --input capture.npz \
  --label approved-capture
```

The dashboard summarizes a local capture and its provenance-aware features.

### Report

```bash
vulture rf-dna report \
  --input capture.npz \
  --label approved-capture
```

The report is suitable for saving to a local file:

```bash
vulture rf-dna report \
  --input capture.npz \
  --label approved-capture > capture-report.json
```

Validate that the output is JSON:

```bash
python -m json.tool capture-report.json
```

### Hash the capture

```bash
sha256sum capture.npz
```

The hash should be stored alongside the capture and report. The hash identifies file contents; it does not identify a transmitter.

---

## Signal-processing concepts

### Windowing

Windowing reduces edge discontinuities before a spectrum calculation. Different windows change the trade-off between leakage and resolution. Results must record the window used.

### FFT and DFT

An FFT or DFT maps samples from the time domain into frequency bins. The sample rate and number of samples determine the bin spacing. A frequency estimate from a coarse capture is not automatically precise.

### PSD

Power spectral density describes power distribution over frequency. It is useful for comparing noise floors and relative spectral energy, but absolute results require proper calibration and known instrument characteristics.

### Spectrogram

A spectrogram applies repeated windowed transforms over time. It can reveal changing frequency content, bursts, and chirps. Segment length, overlap, window type, and scaling should be recorded.

### Waterfall

A waterfall is a visualization of sequential spectra. It is a review surface, not proof that a signal belongs to a particular transmitter.

### Occupancy

Occupancy estimates how often or how strongly a frequency region exceeds a chosen criterion. It depends on thresholds, noise conditions, calibration, and capture duration.

### Peak detection

Peak detection identifies local maxima. A peak is a feature in the supplied data. It is not automatically a protocol, emitter, or identity.

### Noise floor

A noise-floor estimate depends on the capture environment, receiver gain, bandwidth, antenna, filtering, and time period. Compare like with like.

---

## RF-DNA interpretation

RF-DNA features are statistical descriptors extracted from captures. They may include spectral, temporal, power, phase, or other signal features depending on the module.

A fingerprint can support:

- repeatability studies;
- simulator tests;
- comparison of local recordings;
- feature-engineering experiments;
- review of capture consistency.

A fingerprint cannot by itself prove:

- transmitter identity;
- operator identity;
- location;
- intent;
- legal responsibility;
- exclusivity of origin.

Use independent evidence and human review before drawing conclusions.

---

## Offline analysis

The offline toolkit provides local numeric processing:

```bash
vulture offline --help
vulture offline analyze measurements.txt
vulture offline analyze measurements.txt --sample-rate 1000
```

It includes descriptive statistics, peak detection, windowing, DFT, dominant frequency estimation, validation, provenance helpers, uncertainty helpers, and deterministic JSON reporting.

It is useful when a live receiver is unavailable or when a capture must be analyzed in a controlled offline environment.

---

## Interactive shell

The interactive shell is a convenience layer over the command-line functions. It does not add extra hardware behavior.

```bash
vulture --interactive
```

Inside the shell:

```text
> status
> rf-dna status
> rf-dna backends
> rf-dna fingerprint --input capture.npz --label local
> chemical-rf nmr --nucleus 1H --field-t 7
> history
> exit
```

Commands are tokenized with shell-style quoting. JSON arguments should be quoted carefully.

---

## GUI

The optional GUI can provide review surfaces for RF, SDR/IQ, dashboards, visualization, ML, and provenance.

```bash
python -c "from vulture.gui import launch_gui; launch_gui()"
```

The GUI remains optional and headless operation remains supported. A GUI view is an analysis surface, not a transmission interface.

---

## Native C layer

Build the C layer:

```bash
make -C c
```

Clean it:

```bash
make -C c clean
```

Representative commands:

```bash
./vulture_cli status
./vulture_cli demo
./vulture_cli analyze c/sample_signal.txt
./vulture_cli scan 0.1 1.4 0.2 4.8
./vulture_cli hash README.md
./vulture_rf_analysis 2400000000 10
./vulture_hash_engine c/sample_signal.txt
```

The C layer contains scalar signal analysis, hashing, RF math, local IQ analysis, IQ readers, windowing, spectrum helpers, health metrics, reports, self-tests, and narrow interop declarations. It does not automatically connect to an SDR or transmit.

See [`c/README.md`](c/README.md) for the native architecture and build details.

---

## C++ and C# boundaries

The repository includes narrow C-compatible declarations for future wrappers:

- C++ linkage guards preserve C symbol names;
- C#-friendly declarations provide a possible managed ABI boundary;
- wrappers should validate paths, sizes, return codes, and ownership;
- wrappers should preserve the same local-only and receive-only design.

These headers are not a full radio SDK and do not authorize hardware access.

---

## Testing

Run Python tests:

```bash
pytest -q
```

Run coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Run selected tests:

```bash
pytest -q tests/test_cli.py tests/test_forensics.py tests/test_rf_dna.py
```

Build the native layer:

```bash
make -C c clean
make -C c
```

Run basic native checks:

```bash
./vulture_cli status
./vulture_cli demo
./vulture_cli analyze c/sample_signal.txt
./vulture_rf_analysis 1000000000 10
./vulture_hash_engine c/README.md
```

Hardware tests should be enabled only in an explicitly configured authorized laboratory environment:

```bash
RF_DNA_LAB_HARDWARE=1 \
RF_DNA_SOAPY_ARGS='driver=approved-device' \
pytest -q -m hardware tests/test_approved_hardware.py
```

---

## Sanitizers and native validation

Use strict warnings:

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic -O2 \
  -I c \
  -o vulture_cli \
  c/vulture_cli.c c/vulture_core.c -lm
```

Use AddressSanitizer and UndefinedBehaviorSanitizer when available:

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic -g \
  -fsanitize=address,undefined \
  -I c \
  -o vulture_cli_sanitized \
  c/vulture_cli.c c/vulture_core.c -lm
```

Run the sanitized binary:

```bash
./vulture_cli_sanitized status
./vulture_cli_sanitized demo
./vulture_cli_sanitized analyze c/sample_signal.txt
```

For native IQ modules, compile with the same warning and sanitizer policy after the Makefile target includes those modules. Do not treat a successful compile as proof of numerical correctness; use test vectors and expected values as well.

---

## Troubleshooting

### Command not found

Install the package in editable mode and confirm the environment:

```bash
python -m pip install -e .
python -m vulture.cli --help
```

### Chemical-RF help appears without the expected nested commands

The top-level command routes arguments to the Chemical-RF group. Check both entry points:

```bash
vulture chemical-rf --help
vulture-chemical-rf --help
```

### Simulator refuses a request

Check duration, sample rate, and calculated sample count. The simulator intentionally applies resource limits.

### NPZ loading fails

Confirm that the file contains a non-empty `iq` array and a positive `sample_rate` field:

```python
import numpy as np
with np.load("capture.npz") as data:
    print(data.files)
    print(data["iq"].shape)
    print(data["sample_rate"])
```

### SoapySDR is unavailable

The receive adapter is optional. Use a simulator fixture or local NPZ file when the binding is not installed:

```bash
vulture rf-dna simulate --profile noise --output noise.npz
vulture rf-dna fingerprint --input noise.npz --label noise-fixture
```

### Hardware configuration is rejected

Confirm that sample rate is positive, center frequency is non-negative, and explicit device arguments are supplied. Do not remove validation merely to force a connection.

### Frequency results look wrong

Check sample rate, center frequency, sample format, windowing, decimation, and metadata. A correct FFT with incorrect metadata still produces an incorrect interpretation.

### Large files consume too much memory

Use bounded fixtures, shorter captures, or a streaming workflow. Do not raise resource limits blindly.

---

## Project structure

```text
VULTURE/
├── README.md
├── LICENSE
├── pyproject.toml
├── setup.py
├── requirements.txt
├── docs/
├── examples/
├── src/vulture/
│   ├── cli.py
│   ├── gui.py
│   ├── chemical_rf/
│   ├── core/
│   ├── forensics/
│   ├── offline_tools/
│   ├── rf_dna/
│   ├── rf_intelligence/
│   ├── signal_processing/
│   ├── lab/
│   ├── ml_framework/
│   └── visualization_advanced/
├── tests/
├── c/
└── rf_fingerprinting/
```

---

## Safety and limitations

- A fingerprint is a statistical similarity result, not proof of identity.
- A simulation is not a hardware measurement.
- A model prediction is not ground truth.
- An uncalibrated report is not a calibration certificate.
- An RF calculation is not a live link measurement.
- An SDR capture must have appropriate authorization.
- No command should interfere with communications.
- No command should monitor systems without authorization.
- Public package repositories are references and must be reviewed independently.
- Captures may contain sensitive data and should be handled appropriately.

Preserve raw captures, hashes, command lines, configuration, seeds, sample metadata, software versions, and authorization records when reproducibility matters.

---

## Distribution references

- BlackArch radio resources: <https://blackarch.org/radio.html>
- BlackArch package repository: <https://github.com/BlackArch/blackarch-pkgbuilds>
- Pentoo overlay: <https://github.com/pentoo/pentoo-overlay>

These are ecosystem references only. They do not expand VULTURE’s capabilities or change its safety model.

---

## Roadmap

Possible future improvements include:

1. bounded streaming statistics;
2. richer report serialization;
3. stronger IQ format validation;
4. additional window functions;
5. calibrated metadata pathways;
6. native streaming analysis;
7. improved cross-platform build targets;
8. stable C++ and C# wrapper implementations;
9. more simulator profiles;
10. expanded deterministic test vectors;
11. improved provenance schemas;
12. clearer hardware test fixtures.

New features should remain explicit, local, reviewable, dependency-light, and compatible with the receive-only model.

---

## License

VULTURE retains its project identity and existing direction. See [`LICENSE`](LICENSE) for licensing information and project requirements.

**VULTURE: scientific analysis, reproducible evidence, explicit controls, and no unsafe automation.**

