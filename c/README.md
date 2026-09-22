# VULTURE C Layer

> Local, deterministic, receive-only signal analysis in C.
>
> The `c/` directory is the native extension layer for VULTURE. It contains small, reviewable C programs and shared modules for offline signal processing, local evidence hashing, RF calculations, and IQ-based analysis without opening hardware or transmitting anything.

<div align="center">

![Language](https://img.shields.io/badge/language-C11-00599C?style=for-the-badge&logo=c&logoColor=white)
![Mode](https://img.shields.io/badge/mode-offline--deterministic-0A7B5E?style=for-the-badge)
![Safety](https://img.shields.io/badge/signal-analysis-only-6A1B9A?style=for-the-badge)
![Dependencies](https://img.shields.io/badge/dependencies-standard-libc-333333?style=for-the-badge)

</div>

---

## Purpose and scope

The C layer exists to provide a lightweight native implementation for functions that benefit from tight control over memory, predictable behavior, and simple deployment. It is intentionally separated from the Python codebase so the Python platform remains easy to maintain while the C tools remain focused and auditable.

This layer does not:

- open SDR hardware or other devices automatically
- transmit RF energy
- scan networks or contact remote services
- claim calibration, attribution, or operational truth from a single analysis output
- replace the Python platform

The C section is designed around a conservative safety model: values are processed only from explicitly supplied local files or command-line inputs, and the results are descriptive, reproducible, and reviewable.

The goal is not to create a broad autonomous radio platform. The goal is to create a small, understandable set of tools for modeling, signal processing, file integrity checking, and local analysis of supplied evidence. This is a disciplined engineering layer for research, testing, and laboratory workflows where authorized local input must be examined carefully.

---

## Why a C layer exists

Python is excellent for readability, rapid prototyping, and integration. However, certain tasks benefit greatly from a native implementation:

- predictable memory behavior
- compact binaries
- low runtime overhead
- reproducible deterministic computation
- explicit ownership semantics
- easier portability to constrained systems and wrappers
- compatibility with embedded, command-line, or lab automation flows

The C layer answers that need without taking ownership of all of the project behavior. It remains a narrow extension built around explicit inputs and explicit outputs.

This separation is intentional. The Python side remains the primary integration and user-facing interface. The C side exists for performance-sensitive, safer, or more constrained workflows where native code is a better fit.

---

## Safety boundaries

The C layer follows a fail-closed design. It does not create hidden behavior or shadow broader platform capabilities.

Key rules:

- inputs must be explicitly provided by the user or by a local file
- output is descriptive and informational only
- no implicit device access
- no network calls
- no broadcasting or emission logic
- no automatic hardware tuning or scanning loops
- no output that claims identification, attribution, or calibration without metadata
- all functions are reviewable and small enough to inspect by hand

This is important: the native layer is not a broad signal intelligence system. It is an analysis toolkit that consumes data you provide it, in a bounded and explainable way.

---

## Included areas

The C layer currently covers several stable domains:

- signal statistics and peak detection
- file hashing and evidence provenance
- RF calculations such as wavelength and path loss
- local IQ analysis from text-based captures
- deterministic reporting in JSON-like output
- modular code organization for easier extension
- C-compatible interfaces intended for tool integration and future interoperability work

### Core capabilities

| Capability | Description |
| --- | --- |
| Signal summary | Mean, variance, standard deviation, RMS, median, min, max, and peak-to-peak range |
| Peak detection | Local-maxima detection with threshold-based filtering |
| Integrity checks | SHA-256 hashing for file and buffer content |
| RF math | Wavelength and free-space path loss from supplied values |
| IQ analysis | Receive-only IQ metrics from local files |
| Reporting | Deterministic, machine-readable JSON-like output |
| Isolation | Native code remains separate from Python logic and runtime dependencies |
| Interop | C/C++/C# compatibility declarations are deliberately minimal and explicit |

---

## Project layout

```text
c/
├── README.md                    # this guide
├── Makefile                     # native build targets
├── vulture_core.h               # shared public API for core analysis functions
├── vulture_core.c               # signal stats, peak detection, hashing logic
├── vulture_cli.c                # general-purpose native command-line utility
├── vulture_c_features.h         # feature-layer public declarations
├── vulture_c_features.c         # feature-layer implementation and demo suite
├── vulture_sdr.h                # receive-only IQ analysis declarations
├── vulture_sdr.c                # receive-only IQ analysis implementation
├── vulture_c.c                  # command-line wrapper for the C analysis layer
├── vulture_iq_types.h           # shared IQ data structures
├── vulture_iq_types.c           # IQ ownership cleanup
├── vulture_iq_reader.h          # IQ file readers (text and binary)
├── vulture_iq_reader.c          # concrete IQ input loaders
├── vulture_iq_window.h          # windowing abstractions
├── vulture_iq_window.c          # Hann/Hamming support
├── vulture_iq_spectrum.h        # DFT-based dominant frequency analysis
├── vulture_iq_spectrum.c        # spectrum calculations
├── vulture_iq_defense.h         # IQ quality and defensive health metrics
├── vulture_iq_defense.c         # health checks and clipping analysis
├── vulture_iq_report.h          # JSON report interface
├── vulture_iq_report.c          # report serialization
├── vulture_iq.c                 # modular IQ CLI entry point
├── vulture_iq_selftest.h        # self-test declarations
├── vulture_iq_selftest.c        # focused validation checks
├── vulture_cpp.h                # C++ linkage compatibility declarations
├── vulture_csharp_abi.h         # C#-friendly ABI declarations
├── sample_signal.txt            # simple numeric sample input
├── SDR.md                       # IQ analysis notes and usage notes
├── engines/
│   ├── vulture_rf_analysis.c    # wavelength and path-loss engine
│   ├── vulture_hash_engine.c    # file hashing engine
│   └── vulture_iq_analysis.c    # standalone IQ analysis engine
├── translator/
│   └── vulture_tool_translator.c # text-to-C translation helper
├── docs/
│   └── C_UPDATES_AND_FEATURES.md # feature index and engineering notes
└── data/
    └── (optional local analysis fixtures, if added later)
```

This layout keeps each module focused and composable. The goal is not to compress everything into a single enormous source file. Instead, it is easier to reason about the system when each file has a narrow job: reading, windowing, spectrum analysis, health evaluation, report generation, or command-line orchestration.

---

## Build and run

### Requirements

- C11-compatible compiler such as GCC or Clang
- `make`
- standard C library
- `libm` for numerical routines

### Compile the native layer

From the repository root:

```bash
make -C c
```

This creates the native executables in the repository root according to the current build rules, including the general CLI and analysis utilities.

### Clean generated binaries

```bash
make -C c clean
```

----

## Command center

### General native CLI

```bash
./vulture_cli status
./vulture_cli demo
./vulture_cli analyze c/sample_signal.txt
./vulture_cli scan 0.1 1.4 0.2 4.8 0.1 3.2 0.2 5.9
./vulture_cli hash README.md
```

The general CLI reads local values, performs deterministic numerical analysis, and reports results without network access or SDR hardware interaction.

### RF analysis engine

```bash
./vulture_rf_analysis 2400000000 10
```

This tool calculates wavelength and free-space path loss for supplied values only.

### Hash engine

```bash
./vulture_hash_engine c/README.md
```

This produces a SHA-256 digest for local evidence tracking and reproducibility checks.

### IQ analysis

A receive-only IQ analysis command is provided through the C layer for local capture files of the form:

```text
1.0,0.0
0.7,0.7
0.0,1.0
-0.7,0.7
```

Usage pattern:

```bash
./vulture-c analyze capture.txt --sample-rate 1000000
```

The command reports metrics such as:

- DC offset in I and Q
- RMS and mean power
- peak magnitude
- crest factor
- phase statistics
- occupied-bandwidth estimate
- zero-crossing rate
- dominant frequency estimate
- IQ gain imbalance
- IQ correlation
- clipping risk / clip fraction

The output is intentionally descriptive and local-only. It is not a claim of origin, calibration, system identity, or attribution.

---

## What the native tools actually do

The C layer is intentionally conservative and should be understood as a boundary around analysis rather than control.

### 1. Signal statistics

The core signal analysis computes values such as:

- mean
- variance
- standard deviation
- RMS
- median
- minimum and maximum
- peak-to-peak range

These are useful for understanding the distribution and amplitude characteristics of a supplied dataset. They are analytic descriptions, not identifiers.

### 2. Peak detection

The peak detection routines inspect local extrema and compare them against a threshold, which defaults to a simple statistical boundary derived from the signal. This helps identify major local maxima while remaining deterministic and bounded.

### 3. File integrity

SHA-256 is calculated for file contents and buffer content. This supports local evidence tracking, checksums, and reproducibility workflows without external services.

### 4. RF calculations

Local RF calculations include wavelength and free-space path loss based on supplied frequency and distance values. This is purely mathematical and does not use hardware or probes.

### 5. IQ analysis

IQ analysis is intended for local files containing paired in-phase and quadrature samples. The code estimates:

- DC offset
- signal magnitude and power
- signal shape statistics
- dominant frequency content
- signal quality indicators such as correlation and clipping

This is useful for local fixture inspection and deterministic evaluation of supplied captures. The analysis does not infer transmitter configuration or unique device identity.

### 6. File conversion and tooling

The translator utility preserves text content and produces small C programs that can print the preserved content. This is a packaging and operational utility for code generation and translation workflows, not a generalized interpreter.

---

## Data model and file-handling rules

The native layer is designed around a few explicit data structures:

- `SignalBuffer` for scalar numeric arrays
- `SignalStats` for aggregate statistics
- `PeakSummary` for detected extrema
- `VultureIQSample` for complex-valued baseband samples
- `VultureIQSeries` for ordered collections of samples
- `VultureIQHealth` for defensive signal-quality metrics
- `VulturePeak` for dominant spectral detection results

These structures make it easier to reason about memory ownership. Dynamic buffers are freed via dedicated cleanup functions like `vulture_free_signal` and `vulture_iq_series_free`. This reduces leak risk and makes the code easier to inspect.

---

## Input format and examples

### Scalar signal file

```text
0.1 1.4 0.2 4.8 0.1 3.2 0.2 5.9
```

Example usage:

```bash
./vulture_cli analyze c/sample_signal.txt
```

### IQ file

```text
1.0,0.0
0.7,0.7
0.0,1.0
-0.7,0.7
```

Example usage:

```bash
./vulture-c analyze capture.txt --sample-rate 1000000
```

The IQ parser accepts local text input with either comma or whitespace separators in a simple format. The loader checks for finite values and rejects invalid or non-numeric data. This prevents silent corruption and makes debugging easier.

---

## C++ and C# compatibility

The C layer includes compatibility headers that are intentionally narrow and explicit.

### C++ linkage guards

`vulture_cpp.h` is intended to provide protected C linkage for symbols that are exported to C++ code. This helps maintain deterministic ABI behavior when a C function is called from C++ without exposing an uncontrolled object model.

### C#-friendly ABI declarations

`vulture_csharp_abi.h` defines a C ABI surface that can be consumed by managed wrappers or language bindings. The intention is not to create a full managed SDK, but to provide a small, stable, explicit function boundary for external tooling.

These interfaces are intentionally minimal. They are not intended to magically turn the native layer into a general-purpose radio API or exploit surface.

---

## Engineering principles

The native layer follows a deliberately conservative design:

- C11 first: no C++ and no compiler-specific language extensions are required
- Small interfaces: reusable functions are exposed through public headers
- Fail closed: invalid paths, empty signals, allocation failures, and invalid parameters return errors
- Deterministic behavior: calculations use supplied local inputs and stable output formats
- Ownership clarity: dynamically allocated signal buffers are released through explicit cleanup functions
- No destructive operations: analysis tools read inputs and write only explicitly requested outputs
- Safety boundaries: RF functionality remains receive/analyze-only and does not add transmission logic
- Composable programs: each executable has one focused responsibility

For the full update index and future expansion plan, see [`docs/C_UPDATES_AND_FEATURES.md`](docs/C_UPDATES_AND_FEATURES.md).

---

## Recommended validation workflow

Compile with strict warnings during development:

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic -O2 \
  -I c \
  -o vulture_cli \
  c/vulture_cli.c c/vulture_core.c -lm
```

Recommended validation checklist:

```bash
make -C c clean
make -C c
./vulture_cli status
./vulture_cli demo
./vulture_cli analyze c/sample_signal.txt
./vulture_rf_analysis 1000000000 10
./vulture_hash_engine c/README.md
```

For memory-safety testing where available:

```bash
gcc -std=c11 -Wall -Wextra -g -fsanitize=address,undefined \
  -I c -o vulture_cli_sanitized \
  c/vulture_cli.c c/vulture_core.c -lm
```

This remains a strong development pattern because it catches memory issues early, preserves determinism, and makes the native layer easier to maintain.

---

## Extra ecosystem references and context

The VULTURE C layer is not isolated from the wider ecosystem of public tooling and package repositories that include radio and SDR-related projects, but the repository itself remains intentionally conservative. Public package repositories are useful as references for tooling discovery and ecosystem awareness; they are not part of the VULTURE implementation.

The following are public references frequently used by users exploring radio and SDR-related packages in broader Linux security and radio communities:

- BlackArch radio page: https://blackarch.org/radio.html
- BlackArch package build repository: https://github.com/BlackArch/blackarch-pkgbuilds
- Pentoo official overlay: https://github.com/pentoo/pentoo-overlay

These links are relevant as ecosystem references only. They do not change VULTURE’s core design or safety model. The project continues to remain a local, deterministic, receive-only analysis toolkit with explicit limits on what it does and how it behaves.

This distinction matters. A software ecosystem may contain many tools for radio work, but VULTURE remains intentionally narrow and safety-oriented. We do not treat the library as a general-purpose scanning or offensive exploitation system. Instead, the code is built around reproducible local analysis and documented intent.

---

## Documentation map

- [`docs/C_UPDATES_AND_FEATURES.md`](docs/C_UPDATES_AND_FEATURES.md) — feature inventory and engineering notes
- [`../README.md`](../README.md) — project-wide overview
- [`../docs/DUAL_USE_LAB.md`](../docs/DUAL_USE_LAB.md) — authorized lab-use considerations
- [`SDR.md`](SDR.md) — receive-only IQ analysis notes

---

## Future roadmap

The native layer is deliberately designed to be extended in a controlled way. Planned extensions can be added as independent modules:

1. bounded streaming statistics
2. structured report serialization
3. benchmark and profiling harnesses
4. reusable parser utilities
5. test vectors for hashing and numerical analysis
6. optional language adapters with explicit input/output contracts
7. improved IQ file validation and variance diagnostics
8. richer windowing and spectral metrics
9. local sample provenance metadata
10. integration with other deterministic offline toolchains

New features should remain local, reviewable, dependency-light, and compatible with the existing VULTURE safety model.

The roadmap intentionally avoids broad, implicit, or opaquely automatic behaviors. This is a core engineering principle of the C layer.

---

## Overall intent

The C layer is a disciplined extension of VULTURE: it accepts explicit local inputs, performs bounded offline analytics, and emits clear, reproducible reports. Its purpose is to improve performance and clarity where C is a good fit, without introducing broad, unsafe, or implicit operational behavior.

The layer is intentionally conservative, modular, and easy to review.

It is built to serve a clear purpose:

- analyze what is supplied
- emit reproducible outputs
- keep the code honest and inspectable
- remain local and deterministic
- preserve a strong boundary between analysis and control

This is the conceptual center of the C section and the reason it exists as a distinct project layer.

---

<div align="center">

**VULTURE C — transparent, local, and deterministic analysis.**

</div>
