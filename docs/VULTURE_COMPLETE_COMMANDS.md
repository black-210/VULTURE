# VULTURE Complete Terminal Command Guide

This guide covers the **entire main `vulture` command line interface**, not only RF-DNA. It explains what each command does, what is printed after pressing Enter, expected result formats, and whether the command uses hardware or the network.

All examples are designed for authorized, local, offline analysis. Existing commands are preserved.

## Quick command map

```text
vulture
├── info
├── status
├── rf-wavelength
├── rf-path-loss
├── chemical-rf
│   ├── nmr
│   ├── material
│   ├── physics
│   └── report
├── forensic
│   ├── physics
│   ├── chemistry
│   ├── math
│   └── protocol
├── rf-dna
│   ├── status
│   ├── simulate
│   ├── fingerprint
│   ├── dashboard
│   ├── report
│   ├── quantum
│   └── backends
└── --interactive
```

The `rf-dna` group is included in this complete guide for completeness, but this document covers the whole VULTURE CLI: platform status, RF calculations, Chemical-RF analysis, forensics, interactive mode, and RF-DNA.

## Installation and command availability

From the repository root:

```bash
python -m pip install -e .
```

Then verify the installed console entry point:

```bash
vulture --help
```

Expected output includes:

```text
Usage: vulture [OPTIONS] COMMAND [ARGS]...

Options:
  --interactive  Open the interactive > prompt.
  --help         Show this message and exit.

Commands:
  chemical-rf  Route to the Chemical-RF command group.
  forensic     Offline evidence audit commands for supplied local data.
  info         Display platform capabilities.
  rf-dna       Integrated receive-only RF-DNA simulation, analysis, and reporting commands.
  rf-path-loss
  rf-wavelength
  status       Show safe runtime status.
```

The exact help spacing depends on the installed Click version. Pressing Enter after this command only prints help; it does not open hardware or contact a network.

## `vulture info`

Command:

```bash
vulture info
```

Purpose: display the platform's major capabilities.

Expected output:

```text
🦅 VULTURE
Science: chemistry • physics • mathematics • RF
Forensics: offline audit of supplied evidence only
RF-DNA: vulture rf-dna --help
Interactive: vulture --interactive
```

Behavior: local output only. No input file, hardware, or network is required.

## `vulture status`

Command:

```bash
vulture status
```

Purpose: show the safe runtime mode.

Expected output:

```json
{
  "analysis": "local-only",
  "cli": "online",
  "hardware": "not-opened",
  "mode": "offline-deterministic",
  "network": "disabled",
  "rf_dna_command": "vulture rf-dna",
  "rf_transmit": "disabled"
}
```

Behavior: this is a status report, not a hardware test. It does not open an SDR or create a network connection.

## `vulture rf-wavelength`

Command:

```bash
vulture rf-wavelength --frequency-hz 1000000000
```

Purpose: calculate wavelength from frequency.

Expected output:

```json
{
  "frequency_hz": 1000000000.0,
  "wavelength_m": 0.299792458
}
```

Formula:

```text
wavelength = speed_of_light / frequency
```

Invalid or non-positive frequencies are rejected by the underlying science function.

## `vulture rf-path-loss`

Command:

```bash
vulture rf-path-loss --frequency-hz 2400000000 --distance-m 10
```

Purpose: calculate free-space path loss for supplied values.

Expected output shape:

```json
{
  "frequency_hz": 2400000000.0,
  "distance_m": 10.0,
  "path_loss_db": 60.046
}
```

The exact decimal representation comes from the implementation. This command performs a local calculation only; it does not measure a live signal.

# Chemical-RF command group

Use the integrated form:

```bash
vulture chemical-rf --help
```

The available subcommands are `nmr`, `material`, `physics`, and `report`.

## `vulture chemical-rf nmr`

Command:

```bash
vulture chemical-rf nmr --nucleus 1H --field-t 7
```

Purpose: calculate an ideal Larmor frequency.

Expected output shape:

```json
{
  "nucleus": "1H",
  "field_t": 7.0,
  "frequency_hz": 298000000.0
}
```

The exact frequency depends on the nucleus constants in the project. This is an ideal scientific calculation, not a live NMR measurement.

## `vulture chemical-rf material`

Command:

```bash
vulture chemical-rf material \
  --epsilon-r 4.2 \
  --conductivity 0.01 \
  --frequency-hz 2400000000 \
  --length-m 0.1
```

Purpose: calculate complex permittivity and estimate a half-wave dielectric resonance.

Expected output shape:

```json
{
  "permittivity": {
    "real": 4.2,
    "imag": -0.0000000007
  },
  "resonance_hz": 730000000.0
}
```

The exact imaginary component and resonance depend on the supplied values and project constants. No physical material is contacted or controlled.

## `vulture chemical-rf physics`

Command:

```bash
vulture chemical-rf physics \
  --frequency-hz 2400000000 \
  --distance-m 10
```

Purpose: return wavelength and free-space path loss together.

Expected output shape:

```json
{
  "wavelength_m": 0.124913524,
  "path_loss_db": 60.046
}
```

## `vulture chemical-rf report`

Command:

```bash
vulture chemical-rf report \
  --sample-id S-001 \
  --real-ohm 50 \
  --imag-ohm 2.5 \
  --frequency-hz 2400000000
```

Purpose: create an explicitly uncalibrated impedance analysis report.

Expected result structure:

```json
{
  "sample_id": "S-001",
  "impedance": {
    "real_ohm": 50.0,
    "imag_ohm": 2.5
  },
  "metadata": {
    "frequency_hz": 2400000000.0
  },
  "calibrated": false
}
```

The exact fields are produced by `ChemicalRFAnalysisPipeline().analyze_impedance(...).to_dict()`.

# Forensic command group

Show the group help:

```bash
vulture forensic --help
```

Available commands:

```text
physics
chemistry
math
protocol
```

These commands audit supplied local evidence or metadata. They do not connect to targets, capture traffic, or perform active operations.

## `vulture forensic physics`

Command:

```bash
vulture forensic physics \
  --case-id C-001 \
  --subject capture \
  --frequency-hz 2400000000 \
  --distance-m 10
```

Purpose: audit supplied physical measurement metadata.

Expected JSON result shape:

```json
{
  "case_id": "C-001",
  "subject": "capture",
  "status": "passed",
  "checks": [],
  "findings": []
}
```

Optional text output:

```bash
vulture forensic physics \
  --case-id C-001 \
  --subject capture \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --format txt
```

Save a report while still printing it:

```bash
vulture forensic physics \
  --case-id C-001 \
  --subject capture \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --output physics-report.json
```

## `vulture forensic chemistry`

Command:

```bash
vulture forensic chemistry \
  --case-id C-002 \
  --subject sample \
  --compounds-json '[{"elements":{"H":2,"O":1}}]'
```

Purpose: audit local compound composition structures.

Expected result shape:

```json
{
  "case_id": "C-002",
  "subject": "sample",
  "status": "passed",
  "findings": []
}
```

Malformed JSON is rejected instead of being silently interpreted.

## `vulture forensic math`

Command:

```bash
vulture forensic math \
  --case-id C-003 \
  --subject system \
  --matrix-json '[[2,1],[1,1]]' \
  --vector-json '[3,2]'
```

Purpose: audit a supplied linear system.

Expected result shape:

```json
{
  "case_id": "C-003",
  "subject": "system",
  "status": "passed",
  "findings": []
}
```

## `vulture forensic protocol`

Command:

```bash
vulture forensic protocol \
  --case-id C-004 \
  --subject frame \
  --frames-json '[{"length":4,"declared_length":5}]'
```

Purpose: audit supplied protocol/frame metadata without network access.

Expected result shape:

```json
{
  "case_id": "C-004",
  "subject": "frame",
  "status": "warning",
  "findings": [
    "declared length does not match observed length"
  ]
}
```

The exact finding text is generated by the forensic audit implementation.

# Integrated `vulture rf-dna` group

The main CLI also exposes the existing receive-only RF-DNA tools through the `vulture` executable:

```bash
vulture rf-dna --help
```

Commands:

```text
status
simulate
fingerprint
dashboard
report
quantum
backends
```

Examples:

```bash
vulture rf-dna status
vulture rf-dna simulate --profile multi-tone --duration 2 --sample-rate 1000000 --output capture.npz
vulture rf-dna fingerprint --input capture.npz --label lab-device-01
vulture rf-dna dashboard --input capture.npz
vulture rf-dna report --input capture.npz
vulture rf-dna quantum --profile multi-tone
vulture rf-dna backends
```

These commands are documented here because they are part of the complete CLI. They remain local-first, bounded, and receive-only.

# Interactive mode

Start the interactive terminal:

```bash
vulture --interactive
```

Example session:

```text
🦅 VULTURE — Offline Scientific Intelligence Platform
chemistry • physics • mathematics • RF • forensic audit
Type: help | status | rf-dna status | forensic physics | exit
> help
Available commands:
  info
  status
  rf-wavelength --frequency-hz 1e9
  rf-path-loss --frequency-hz 2.4e9 --distance-m 10
  rf-dna status
  rf-dna simulate --profile multi-tone --duration 2 --sample-rate 1000000 --output capture.npz
  chemical-rf nmr --nucleus 1H --field-t 7
  forensic physics --case-id C-001 --subject capture --frequency-hz 2.4e9 --distance-m 10
  history
  exit
> status
{
  "analysis": "local-only",
  "cli": "online",
  "hardware": "not-opened",
  "mode": "offline-deterministic",
  "network": "disabled",
  "rf_transmit": "disabled"
}
> history
1: help
2: status
> exit
✓ Session closed safely.
```

Pressing Enter with an empty line does nothing. `help` prints commands, `history` shows previous commands, and `exit` or `quit` closes the shell.

# Testing commands

Run the complete test suite:

```bash
pytest -q
```

Expected successful format:

```text
........................................................                 [100%]
XX passed, Y skipped in <time>s
```

`XX` and `Y` are intentionally variable because the repository can gain tests over time.

Run coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Run selected CLI and forensic tests:

```bash
pytest -q tests/test_cli.py tests/test_forensics.py tests/test_rf_dna.py
```

# Error and validation behavior

Examples of expected validation failures:

```bash
vulture rf-wavelength --frequency-hz 0
```

```text
Error: frequency must be positive
```

```bash
vulture forensic math --case-id C-003 --subject system --matrix-json 'bad' --vector-json '[1]'
```

```text
Error: invalid JSON
```

Missing required options are reported by Click:

```text
Error: Missing option '--frequency-hz'.
```

The CLI fails closed on invalid input instead of inventing scientific results.

# What happens when Enter is pressed

For a normal command:

1. The `vulture` entry point loads `vulture.cli:cli`.
2. Click parses the command and options.
3. Input validation runs.
4. The selected local calculation or audit runs.
5. JSON or text is printed.
6. The process exits with a success or error code.

For interactive mode:

1. The banner appears.
2. The `>` prompt waits for input.
3. Pressing Enter submits the current line.
4. The command is parsed and executed locally.
5. The next prompt appears unless `exit` or `quit` was entered.

# Safety and scope

The VULTURE CLI is intended for authorized scientific, defensive, and forensic work:

- calculations use supplied values;
- forensic commands inspect supplied local evidence;
- optional SDR support is explicit and receive-only;
- remote service operation requires authentication and TLS;
- no command transmits RF;
- no command performs jamming or spoofing;
- no command performs arbitrary network probing.

# Actual output versus documentation examples

The result structures shown here match the current command interfaces. Exact floating-point values, hashes, test counts, dependency status, and forensic findings depend on the input and environment. When producing an official record, save the real terminal output rather than copying an illustrative value from this guide.
