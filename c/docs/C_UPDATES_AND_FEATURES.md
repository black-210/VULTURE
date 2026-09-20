# VULTURE C Engineering Layer

This directory contains the C-based extension layer for VULTURE. It adds standalone C programs, engine components, data-analysis utilities, and translation tooling while preserving the existing Python project structure and functionality.

## Contents

- `vulture_core.h` and `vulture_core.c` — shared C engine core with signal statistics, peak detection, and SHA-256 hashing
- `vulture_cli.c` — command-line access for status, hashing, signal analysis, and demo routines
- `translator/vulture_tool_translator.c` — utility that reads an input tool file and emits C source that preserves the original tool text as translated C strings
- `engines/vulture_rf_analysis.c` — RF wavelength and free-space-loss analysis in C
- `engines/vulture_hash_engine.c` — standalone hashing utility
- `docs/C_UPDATES_AND_FEATURES.md` — dedicated documentation of the new updates, capabilities, and C expertise

## High-value features added

- C-only analytics for numerical data streams
- Peak detection and statistical analysis for signal-like data
- SHA-256 hashing for file and buffer inputs
- RF analysis in plain C for wavelength and path-loss calculations
- Tool-to-C translation utility to preserve content as translated C source
- Modular project layout for future C expansions

## Usage

From the repo root:

```bash
make -C c
./c/vulture_cli status
./c/vulture_cli hash README.md
./c/vulture_cli analyze c/sample_signal.txt
./c/vulture_tool_translator input.txt output.c
./c/vulture_rf_analysis 2400000000 10
./c/vulture_hash_engine README.md
```

## Safety and design notes

- No existing Python files were deleted or modified.
- All additions are isolated to the `c/` area.
- Programs are deterministic, local, and analysis-only.
- The C layer is designed to coexist cleanly with the existing VULTURE platform.

## Directory and feature roadmap

- `c/core` → future core libraries
- `c/engines` → domain-specific analysis programs
- `c/translator` → tool/asset translation utilities
- `c/docs` → technical documentation and implementation notes

## Implementation principle

The C layer follows the same VULTURE philosophy: local-only analysis, deterministic output, explicit validation, and strong separation from unsafe automation.
