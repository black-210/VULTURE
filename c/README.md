# 🦅 VULTURE C Extension Layer

> **Fast. Deterministic. Local. Built in C.**
>
> A focused native toolkit for signal analytics, RF calculations, file integrity, and tool-to-C translation — designed to extend VULTURE without disturbing the existing Python platform.

<div align="center">

![Language](https://img.shields.io/badge/language-C11-00599C?style=for-the-badge&logo=c&logoColor=white)
![Mode](https://img.shields.io/badge/mode-offline--deterministic-0A7B5E?style=for-the-badge)
![Safety](https://img.shields.io/badge/RF-receive%20%26%20analyze%20only-6A1B9A?style=for-the-badge)
![Dependencies](https://img.shields.io/badge/dependencies-standard%20library-333333?style=for-the-badge)

</div>

---

## ✨ What this layer adds

The `c/` directory is VULTURE's standalone native analysis layer. It provides small, composable C programs that can be compiled independently and used from scripts, terminals, laboratories, or future integrations.

### Core capabilities

| Capability | Description |
| --- | --- |
| **Signal intelligence** | Mean, variance, standard deviation, RMS, median, range, and peak-to-peak analysis |
| **Peak detection** | Local-maxima detection with automatic statistical thresholds |
| **Evidence integrity** | SHA-256 hashing for files and memory buffers |
| **RF mathematics** | Wavelength and free-space path-loss calculations |
| **Tool translation** | Converts text-based tool content into compilable C string data |
| **Portable reports** | Stable JSON-like output for offline review and automation |

> Results are analytical outputs, not proof of identity, attribution, or legal conclusions. Use only data and frequencies you own or are authorized to analyze.

---

## 🗂️ Project map

```text
c/
├── README.md                         ← this guide
├── Makefile                          ← native build targets
├── vulture_core.h                    ← shared public API
├── vulture_core.c                    ← shared analytics and SHA-256 engine
├── vulture_cli.c                     ← general-purpose C command line
├── sample_signal.txt                 ← sample numeric input
├── engines/
│   ├── vulture_rf_analysis.c         ← RF wavelength/path-loss engine
│   └── vulture_hash_engine.c         ← standalone file hashing tool
├── translator/
│   └── vulture_tool_translator.c     ← text-to-C translation utility
└── docs/
    └── C_UPDATES_AND_FEATURES.md     ← C feature and expertise index
```

The native layer is intentionally isolated. Existing Python, documentation, tests, and project behavior remain separate and are not replaced by these additions.

---

## 🚀 Build

### Requirements

- A C11-compatible compiler such as GCC or Clang
- `make`
- Standard C library
- `libm` for the RF analysis executable

### Compile every C program

From the repository root:

```bash
make -C c
```

Executables are produced in the repository root by the current Makefile:

```text
vulture_cli
vulture_tool_translator
vulture_rf_analysis
vulture_hash_engine
```

Clean generated binaries:

```bash
make -C c clean
```

---

## 🧰 Command center

### Check native status

```bash
./vulture_cli status
```

### Analyze a numeric signal

```bash
./vulture_cli analyze c/sample_signal.txt
```

The analyzer reports descriptive statistics and detected peaks without opening hardware, using a network, or modifying the input.

### Analyze values directly

```bash
./vulture_cli scan 0.1 1.4 0.2 4.8 0.1 3.2 0.2 5.9
```

### Hash a file

```bash
./vulture_cli hash README.md
./vulture_hash_engine c/sample_signal.txt
```

Both tools produce a lowercase SHA-256 digest suitable for local evidence tracking and reproducibility checks.

### Run the built-in demonstration

```bash
./vulture_cli demo
```

---

## 📡 RF analysis

The RF engine performs bounded mathematical calculations only:

```bash
./vulture_rf_analysis 2400000000 10
```

Example output shape:

```json
{
  "frequency_hz": 2400000000.000000000000,
  "distance_m": 10.000000000000,
  "wavelength_m": 0.124913524167,
  "free_space_path_loss_db": 60.045997...
}
```

This program does **not** transmit, scan, contact a target, or control SDR hardware. It is a local calculator for supplied values.

---

## 🔁 Tool-to-C translator

The translator converts a text-based tool, note, or asset into a small C program that prints the preserved non-empty lines:

```bash
./vulture_tool_translator input.txt translated_output.c
gcc -std=c11 -Wall -Wextra -pedantic -o translated_output translated_output.c
./translated_output
```

This is a preservation and packaging utility. It does not interpret arbitrary source code, execute input content, or claim to automatically rewrite every programming language into equivalent C semantics.

---

## 🧠 C engineering principles

The native layer follows a deliberately conservative design:

- **C11 first:** no C++ and no compiler-specific language extensions are required.
- **Small interfaces:** reusable functions are exposed through `vulture_core.h`.
- **Fail closed:** invalid paths, empty signals, allocation failures, and invalid parameters return errors.
- **Deterministic behavior:** calculations use supplied local inputs and stable output formats.
- **Ownership clarity:** dynamically allocated signal buffers are released through `vulture_free_signal`.
- **No destructive operations:** analysis tools read inputs and write only explicitly requested outputs.
- **Safety boundaries:** RF functionality remains receive/analyze-only and does not add transmission logic.
- **Composable programs:** each executable has one focused responsibility.

For the full update index and future expansion plan, see [`docs/C_UPDATES_AND_FEATURES.md`](docs/C_UPDATES_AND_FEATURES.md).

---

## 🛠️ Development workflow

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

---

## 📚 Documentation

- [`docs/C_UPDATES_AND_FEATURES.md`](docs/C_UPDATES_AND_FEATURES.md) — feature inventory, directory map, and C expertise notes
- [`../README.md`](../README.md) — complete VULTURE platform guide
- [`../docs/DUAL_USE_LAB.md`](../docs/DUAL_USE_LAB.md) — authorized laboratory-use guidance

---

## 🧭 Roadmap

Planned extensions can be added as independent C modules:

1. bounded streaming statistics
2. structured report serialization
3. benchmark and profiling harnesses
4. reusable parser utilities
5. test vectors for hashing and numerical analysis
6. optional language adapters with explicit input/output contracts

New features should remain local, reviewable, dependency-light, and compatible with the existing VULTURE safety model.

---

<div align="center">

**VULTURE C — native analysis with discipline.**

</div>
