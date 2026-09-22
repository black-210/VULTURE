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

---

## What is included

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

---

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

## Safety and engineering principles

The C layer follows a deliberately minimal and safe design model:

- C11-first implementation with standard libraries only
- small, composable modules with explicit interfaces
- no automatic hardware probing or device discovery
- deterministic behavior from supplied local input
- fail-closed error handling for invalid files and invalid parameters
- memory ownership through clear cleanup functions
- local-only output and no remote connectivity assumptions
- no claims of operational capability beyond the input data provided

This makes the C extension layer a useful complement to the main Python platform while keeping the responsibilities and risks clearly bounded.

---

## Interop and compatibility notes

The native layer also contains compatibility definitions designed for external tool integration:

- `vulture_cpp.h` provides C++ linkage guards around C symbols
- `vulture_csharp_abi.h` provides a C-ABI-friendly surface for use in a managed integration layer

These are intentionally kept simple and explicit. They do not add remote connectivity or hidden execution paths.

---

## Documentation map

- [`docs/C_UPDATES_AND_FEATURES.md`](docs/C_UPDATES_AND_FEATURES.md) — feature inventory and engineering notes
- [`../README.md`](../README.md) — project-wide overview
- [`../docs/DUAL_USE_LAB.md`](../docs/DUAL_USE_LAB.md) — authorized lab-use considerations
- [`SDR.md`](SDR.md) — receive-only IQ analysis notes

---

## Recommended validation workflow

```bash
make -C c clean
make -C c
./vulture_cli status
./vulture_cli demo
./vulture_cli analyze c/sample_signal.txt
./vulture_rf_analysis 1000000000 10
./vulture_hash_engine c/README.md
```

For stricter runtime validation when available:

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic -g -fsanitize=address,undefined \
  -I c -o vulture_cli_sanitized \
  c/vulture_cli.c c/vulture_core.c -lm
```

---

## Overall intent

The C layer is a disciplined extension of VULTURE: it accepts explicit local inputs, performs bounded offline analytics, and emits clear, reproducible reports. Its purpose is to improve performance and clarity where C is a good fit, without introducing broad, unsafe, or implicit operational behavior.

The layer is intentionally conservative, modular, and easy to review.

---

<div align="center">

**VULTURE C — transparent, local, and deterministic analysis.**

</div>
