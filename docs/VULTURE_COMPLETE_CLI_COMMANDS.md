# VULTURE Complete CLI Command Reference

This file matches the actual Click command tree defined in the project source and the installed console scripts in `pyproject.toml`.

Canonical CLI entrypoints:
- `vulture`
- `vulture-chemical-rf`
- `vulture-rf-dna`

The command wiring is registered in:
- `src/vulture/cli.py`
- `src/vulture/forensic_cli.py`
- `src/vulture/iq_cli.py`
- `src/vulture/lab_cli.py`
- `src/vulture/offline_tools/cli.py`
- `src/vulture/rf_dna/cli.py`
- `src/vulture/chemical_rf/cli.py`

The command surface is intentionally receive-only and local-analysis focused, with no hardware or RF transmit execution.

---

## Table of contents

1. [Root CLI commands](#root-cli-commands)
2. [Chemical-RF commands](#chemical-rf-commands)
3. [RF-Vuln commands](#rf-vuln-commands)
4. [RF-DNA commands](#rf-dna-commands)
5. [Forensic commands](#forensic-commands)
6. [Lab commands](#lab-commands)
7. [IQ commands](#iq-commands)
8. [Offline commands](#offline-commands)
9. [Quick examples](#quick-examples)

---

## Root CLI commands

### `vulture --help`

Shows the root command tree and available entrypoints.

```bash
vulture --help
```

### `vulture info`

Prints the platform capabilities and the module names exposed by the CLI.

```bash
vulture info
```

### `vulture status`

Returns the safe runtime status payload.

```bash
vulture status
```

Example JSON shape:

```json
{
  "cli": "online",
  "mode": "offline-deterministic",
  "hardware": "not-opened",
  "network": "disabled",
  "rf_transmit": "disabled",
  "analysis": "local-only",
  "rf_dna_command": "vulture rf-dna",
  "rf_vuln_command": "vulture rf-vuln",
  "capture_formats": ["npz", "iq"],
  "forensic_formats": ["npz", "iq"],
  "sdr_mode": "receive-only"
}
```

### `vulture --interactive`

Launches the local interactive shell.

```bash
vulture --interactive
```

Within the shell:

```text
> help
> status
> forensic physics --case-id C-001 --subject test --frequency-hz 2400000000 --distance-m 10
> chemical-rf wavelength --frequency-hz 2400000000
> exit
```

---

## Chemical-RF commands

These are available under the root command group `vulture chemical-rf` and also via the installed script `vulture-chemical-rf`.

### `vulture chemical-rf nmr`

Offline NMR spectroscopy analysis from a local capture file.

```bash
vulture chemical-rf nmr \
  --input capture.npz \
  --nucleus 1H \
  --field-t 7.0
```

Options:
- `--input` (required): local `.npz` or `.iq` capture
- `--nucleus` (default: `1H`)
- `--field-t` (default: `7.0`) in tesla

### `vulture chemical-rf path-loss`

Calculate free-space path loss in dB.

```bash
vulture chemical-rf path-loss \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --antenna-gain-dbi 0.0
```

Options:
- `--frequency-hz` (required)
- `--distance-m` (required)
- `--antenna-gain-dbi` (default: `0.0`)

### `vulture chemical-rf wavelength`

Calculate wavelength from supplied frequency.

```bash
vulture chemical-rf wavelength --frequency-hz 2400000000
```

Options:
- `--frequency-hz` (required)

### `vulture chemical-rf` (group help)

```bash
vulture chemical-rf --help
```

---

## RF-Vuln commands

### `vulture rf-vuln device`

Run offline device compromise analysis against a local capture.

```bash
vulture rf-vuln device \
  --input capture.npz \
  --case-id C-001 \
  --subject device-01 \
  --frequency-hz 433920000 \
  --format json
```

Options:
- `--input` (required)
- `--case-id` (required)
- `--subject` (required)
- `--frequency-hz` (required)
- `--output` (optional file path)
- `--format` (`json`, `txt`, or `html`; default `json`)

### `vulture rf-vuln report`

Write a vulnerability report to disk.

```bash
vulture rf-vuln report \
  --input capture.npz \
  --case-id C-001 \
  --subject device-01 \
  --frequency-hz 433920000 \
  --output report.json \
  --format json
```

### `vulture rf-vuln --help`

```bash
vulture rf-vuln --help
```

---

## RF-DNA commands

These are available through the root CLI as `vulture rf-dna` and also via the installed script `vulture-rf-dna`.

### `vulture rf-dna status`

```bash
vulture rf-dna status
```

### `vulture rf-dna simulate`

Generate a deterministic synthetic IQ capture without any SDR or network access.

```bash
vulture rf-dna simulate \
  --profile multi-tone \
  --duration 2 \
  --sample-rate 1000000 \
  --seed 7 \
  --output capture.npz
```

Options:
- `--profile` (default `noise`)
- `--duration` (default `1.0`)
- `--sample-rate` (default `1000000`)
- `--seed` (default `7`)
- `--output` (required)

### `vulture rf-dna fingerprint`

Extract a descriptive fingerprint from a local NPZ capture.

```bash
vulture rf-dna fingerprint --input capture.npz --label lab-device-01
```

Options:
- `--input` (required)
- `--label` (default `unlabelled`)

### `vulture rf-dna dashboard`

Generate a locally derived provenance dashboard summary.

```bash
vulture rf-dna dashboard --input capture.npz --label capture-1
```

### `vulture rf-dna report`

Generate a machine-readable RF-DNA report.

```bash
vulture rf-dna report --input capture.npz --label report-001
```

### `vulture rf-dna quantum`

Run a deterministic quantum-inspired RF baseline experiment.

```bash
vulture rf-dna quantum \
  --profile multi-tone \
  --duration 2 \
  --sample-rate 1000000 \
  --seed 7
```

### `vulture rf-dna backends`

Report optional receive-backend availability without probing hardware.

```bash
vulture rf-dna backends
```

### `vulture rf-dna --help`

```bash
vulture rf-dna --help
```

---

## Forensic commands

### `vulture forensic physics`

Check physical measurement plausibility from supplied local values.

```bash
vulture forensic physics \
  --case-id C-001 \
  --subject test \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --bandwidth-hz 20000000
```

Options:
- `--case-id` (required)
- `--subject` (required)
- `--frequency-hz` (required)
- `--distance-m` (required)
- `--bandwidth-hz` (optional)
- `--output` (optional)
- `--format` (`json` or `txt`; default `json`)

### `vulture forensic chemistry`

Audit local compound-composition data.

```bash
vulture forensic chemistry \
  --case-id C-002 \
  --subject sample \
  --compounds-json '[{"elements":{"H":2,"O":1}}]'
```

### `vulture forensic math`

Check a local matrix/vector system for plausibility.

```bash
vulture forensic math \
  --case-id C-003 \
  --subject system \
  --matrix-json '[[2,1],[1,1]]' \
  --vector-json '[3,2]'
```

### `vulture forensic protocol`

Audit supplied protocol/frame metadata.

```bash
vulture forensic protocol \
  --case-id C-004 \
  --subject frame \
  --frames-json '[{"length":4,"declared_length":4}]'
```

### `vulture forensic device`

Run device compromise analysis from a local capture file.

```bash
vulture forensic device \
  --input capture.npz \
  --case-id C-005 \
  --subject device-01 \
  --frequency-hz 433920000 \
  --format json
```

Options:
- `--input` (required)
- `--case-id` (required)
- `--subject` (required)
- `--frequency-hz` (required)
- `--output` (optional)
- `--format` (`json`, `txt`, or `html`; default `json`)

### `vulture forensic report`

Write a forensic report to disk.

```bash
vulture forensic report \
  --input capture.npz \
  --case-id C-005 \
  --subject device-01 \
  --frequency-hz 433920000 \
  --output forensic-report.json \
  --format json
```

### `vulture forensic vulnerability`

Alias for forensic device compromise analysis.

```bash
vulture forensic vulnerability \
  --input capture.npz \
  --case-id C-005 \
  --subject device-01 \
  --frequency-hz 433920000
```

### `vulture forensic --help`

```bash
vulture forensic --help
```

---

## Lab commands

### `vulture lab attack-sim`

Run a local synthetic attack simulation with no live target or transmitter.

```bash
vulture lab attack-sim --scenario spoofing --seed 7
```

Allowed scenarios:
- `rf-jamming`
- `spoofing`
- `injection`
- `protocol-abuse`

### `vulture lab defense-sim`

Run a local synthetic defense simulation.

```bash
vulture lab defense-sim --scenario jamming-detection --seed 11
```

Allowed scenarios:
- `jamming-detection`
- `spoof-detection`
- `protocol-anomaly`
- `chemical-rf-drift`

### `vulture lab --help`

```bash
vulture lab --help
```

---

## IQ commands

### `vulture iq convert`

Convert a canonical `.iq` file into `.npz` with provenance metadata.

```bash
vulture iq convert capture.iq capture.npz --source recorded_iq --overwrite
```

Arguments:
- `INPUT_PATH` (required)
- `OUTPUT_PATH` (required)

Options:
- `--source` (default `recorded_iq`)
- `--overwrite` (flag)

### `vulture iq --help`

```bash
vulture iq --help
```

---

## Offline commands

### `vulture offline analyze`

Analyze numeric values from a local CSV or whitespace-delimited file.

```bash
vulture offline analyze values.csv --sample-rate 1000000
```

Arguments:
- `PATH` (required): local analysis file

Options:
- `--sample-rate` (optional)

### `vulture offline --help`

```bash
vulture offline --help
```

---

## Quick examples

### Main entrypoints

```bash
vulture --help
vulture info
vulture status
vulture --interactive
```

### RF and science commands

```bash
vulture chemical-rf wavelength --frequency-hz 2400000000
vulture chemical-rf path-loss --frequency-hz 2400000000 --distance-m 10
vulture rf-dna simulate --profile multi-tone --duration 2 --sample-rate 1000000 --seed 7 --output capture.npz
vulture rf-dna fingerprint --input capture.npz --label lab-device-01
```

### Forensic and evidence checks

```bash
vulture forensic device --input capture.npz --case-id C-005 --subject device-01 --frequency-hz 433920000
vulture forensic report --input capture.npz --case-id C-005 --subject device-01 --frequency-hz 433920000 --output report.json --format json
```

### File conversion and local analysis

```bash
vulture iq convert capture.iq capture.npz --source recorded_iq --overwrite
vulture offline analyze values.csv --sample-rate 1000000
```

This reference intentionally mirrors the actual CLI definitions and should remain aligned with the command groups registered in the source tree.
