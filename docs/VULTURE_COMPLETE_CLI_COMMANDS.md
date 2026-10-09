# VULTURE Complete CLI Command Reference

**Canonical entrypoints:**
- `vulture` (main CLI)
- `vulture-chemical-rf` (chemical-rf CLI)
- `vulture-rf-dna` (RF-DNA CLI)

**Source implementations:**
- `src/vulture/cli.py` - Root command group
- `src/vulture/forensic_cli.py` - Forensic subcommand group
- `src/vulture/lab_cli.py` - Lab subcommand group
- `src/vulture/iq_cli.py` - IQ subcommand group
- `src/vulture/offline_tools/cli.py` - Offline subcommand group
- `src/vulture/rf_dna/cli.py` - RF-DNA command group
- `src/vulture/chemical_rf/cli.py` - Chemical-RF command group

All commands operate **offline-only** with no hardware or RF transmission.

---

## Table of Contents

1. [Root CLI commands](#root-cli-commands)
2. [Chemical-RF commands](#chemical-rf-commands)
3. [RF-Vuln commands](#rf-vuln-commands)
4. [RF-DNA commands](#rf-dna-commands)
5. [Forensic commands](#forensic-commands)
6. [Lab commands](#lab-commands)
7. [IQ commands](#iq-commands)
8. [Offline commands](#offline-commands)
9. [Quick reference](#quick-reference)

---

## Root CLI commands

### `vulture --help`

Shows the root command tree and available subcommands.

```bash
vulture --help
```

**Registered subcommands:**
- `lab` - Authorized laboratory simulations
- `iq` - IQ file conversion
- `offline` - Standalone offline analysis
- `forensic` - Offline evidence audit
- `rf-dna` - RF fingerprinting and DNA analysis
- `info` - Display platform capabilities
- `status` - Show safe runtime status
- `chemical-rf` - Chemistry and RF analysis

---

### `vulture info`

Displays platform capabilities and available modules.

```bash
vulture info
```

**Output:**
```
🦅 VULTURE
Science: chemistry • physics • mathematics • RF
Forensics: offline audit of supplied evidence only
Formats supported: .npz, .iq (all analysis commands)
SDR Receiver: receive-only mode for RTL-SDR, HackRF, USRP
RF-DNA: vulture rf-dna --help
RF-Vulnerability: vulture rf-vuln --help
Chemical-RF: vulture chemical-rf --help
Forensic: vulture forensic --help
IQ: vulture iq --help (convert .iq ↔ .npz)
Offline analysis: vulture offline --help
Lab: vulture lab --help
Interactive: vulture --interactive
```

---

### `vulture status`

Reports the safe runtime status and confirms offline mode.

```bash
vulture status
```

**JSON Output:**
```json
{
  "analysis": "local-only",
  "capture_formats": ["npz", "iq"],
  "cli": "online",
  "forensic_formats": ["npz", "iq"],
  "hardware": "not-opened",
  "mode": "offline-deterministic",
  "network": "disabled",
  "rf_dna_command": "vulture rf-dna",
  "rf_transmit": "disabled",
  "rf_vuln_command": "vulture rf-vuln",
  "sdr_mode": "receive-only"
}
```

---

### `vulture --interactive`

Launches the interactive shell with a `>` prompt for live command input.

```bash
vulture --interactive
```

**Example session:**
```
> help
> status
> forensic physics --case-id C-001 --subject test --frequency-hz 2.4e9 --distance-m 10
> chemical-rf wavelength --frequency-hz 2.4e9
> exit
```

---

## Chemical-RF commands

Available via `vulture chemical-rf` or the installed script `vulture-chemical-rf`.

### `vulture chemical-rf nmr`

Offline NMR spectroscopy analysis from a local capture file.

```bash
vulture chemical-rf nmr \
  --input capture.npz \
  --nucleus 1H \
  --field-t 7.0
```

**Options:**
- `--input` (required): `.npz` or `.iq` capture file
- `--nucleus` (default: `1H`): Nucleus type
- `--field-t` (default: `7.0`): Magnetic field in Tesla

**Output:** JSON with Larmor frequency and capture metadata

---

### `vulture chemical-rf path-loss`

Calculate free-space path loss in dB.

```bash
vulture chemical-rf path-loss \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --antenna-gain-dbi 0.0
```

**Options:**
- `--frequency-hz` (required): Frequency in Hz
- `--distance-m` (required): Distance in meters
- `--antenna-gain-dbi` (default: `0.0`): Antenna gain in dBi

**Output:** JSON with path loss in dB

---

### `vulture chemical-rf wavelength`

Calculate wavelength from supplied frequency.

```bash
vulture chemical-rf wavelength --frequency-hz 2400000000
```

**Options:**
- `--frequency-hz` (required): Frequency in Hz

**Output:** JSON with wavelength in meters

---

## RF-Vuln commands

### `vulture rf-vuln device`

Run forensic device compromise analysis against an offline capture.

```bash
vulture rf-vuln device \
  --input capture.npz \
  --case-id C-001 \
  --subject device-01 \
  --frequency-hz 433920000 \
  --format json
```

**Options:**
- `--input` (required): `.npz` or `.iq` capture file
- `--case-id` (required): Case identifier
- `--subject` (required): Device/subject identifier
- `--frequency-hz` (required): Center frequency in Hz
- `--output` (optional): File path for report
- `--format` (default: `json`): `json`, `txt`, or `html`

**Output:** Compromise analysis with vulnerability findings and evidence hash

---

### `vulture rf-vuln report`

Write RF vulnerability assessment report to disk.

```bash
vulture rf-vuln report \
  --input capture.npz \
  --case-id C-001 \
  --subject device-01 \
  --frequency-hz 433920000 \
  --output report.json \
  --format json
```

**Options:**
- All options from `rf-vuln device`
- `--output` (required): Output file path

**Output:** "✓ Report saved to [path]" with evidence hash

---

## RF-DNA commands

Available via `vulture rf-dna` or the installed script `vulture-rf-dna`.

### `vulture rf-dna status`

Return the safe status payload for the RF-DNA tool.

```bash
vulture rf-dna status
```

**Output:** JSON with status and capabilities

---

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

**Options:**
- `--profile` (default: `noise`): `noise` or `multi-tone`
- `--duration` (default: `1.0`): Duration in seconds
- `--sample-rate` (default: `1000000`): Sample rate in Hz
- `--seed` (default: `7`): Random seed
- `--output` (required): Output `.npz` file path

**Output:** JSON with output path, sample count, profile, and seed

---

### `vulture rf-dna fingerprint`

Extract a descriptive fingerprint from a local NPZ capture.

```bash
vulture rf-dna fingerprint \
  --input capture.npz \
  --label device-01
```

**Options:**
- `--input` (required): Input capture file
- `--label` (default: `unlabelled`): Device label

**Output:** JSON fingerprint with metrics and source

---

### `vulture rf-dna dashboard`

Create a dashboard summary and provenance report from a local capture.

```bash
vulture rf-dna dashboard \
  --input capture.npz \
  --label capture-1
```

**Options:**
- `--input` (required): Input capture file
- `--label` (default: `dashboard-capture`): Label

**Output:** JSON dashboard summary with capture metadata

---

### `vulture rf-dna report`

Create a machine-readable RF-DNA report from a local capture.

```bash
vulture rf-dna report \
  --input capture.npz \
  --label report-001
```

**Options:**
- `--input` (required): Input capture file
- `--label` (default: `capture-report`): Label

**Output:** JSON RF-DNA report with fingerprint and analysis

---

### `vulture rf-dna quantum`

Run a deterministic quantum-inspired RF baseline against a classical reference.

```bash
vulture rf-dna quantum \
  --profile multi-tone \
  --duration 2 \
  --sample-rate 1000000 \
  --seed 7
```

**Options:**
- `--profile` (default: `multi-tone`): Signal profile
- `--duration` (default: `2.0`): Duration in seconds
- `--sample-rate` (default: `1000000`): Sample rate in Hz
- `--seed` (default: `7`): Random seed

**Output:** JSON with quantum experiment results and classical baseline

---

### `vulture rf-dna backends`

Report optional receive backends without probing hardware or networks.

```bash
vulture rf-dna backends
```

**Output:** JSON indicating SoapySDR availability and offline mode

---

## Forensic commands

### `vulture forensic physics`

Check physical measurement plausibility without accessing hardware.

```bash
vulture forensic physics \
  --case-id C-001 \
  --subject test \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --bandwidth-hz 20000000
```

**Options:**
- `--case-id` (required): Case identifier
- `--subject` (required): Subject identifier
- `--frequency-hz` (required): Frequency in Hz
- `--distance-m` (required): Distance in meters
- `--bandwidth-hz` (optional): RF bandwidth in Hz
- `--output` (optional): File path
- `--format` (default: `json`): `json` or `txt`

**Output:** JSON audit results

---

### `vulture forensic chemistry`

Check local compound composition data for invalid values.

```bash
vulture forensic chemistry \
  --case-id C-002 \
  --subject sample \
  --compounds-json '[{"elements":{"H":2,"O":1}}]'
```

**Options:**
- `--case-id` (required): Case identifier
- `--subject` (required): Subject identifier
- `--compounds-json` (required): JSON array of compounds
- `--output` (optional): File path
- `--format` (default: `json`): `json` or `txt`

**Output:** JSON audit results with composition validation

---

### `vulture forensic math`

Check a local linear system for dimensions and non-finite values.

```bash
vulture forensic math \
  --case-id C-003 \
  --subject system \
  --matrix-json '[[2,1],[1,1]]' \
  --vector-json '[3,2]'
```

**Options:**
- `--case-id` (required): Case identifier
- `--subject` (required): Subject identifier
- `--matrix-json` (required): JSON matrix array
- `--vector-json` (required): JSON vector array
- `--output` (optional): File path
- `--format` (default: `json`): `json` or `txt`

**Output:** JSON audit results with system validation

---

### `vulture forensic protocol`

Check supplied protocol metadata and frames; no network probing occurs.

```bash
vulture forensic protocol \
  --case-id C-004 \
  --subject frame \
  --frames-json '[{"length":4,"declared_length":4}]'
```

**Options:**
- `--case-id` (required): Case identifier
- `--subject` (required): Subject identifier
- `--frames-json` (required): JSON frame array
- `--output` (optional): File path
- `--format` (default: `json`): `json` or `txt`

**Output:** JSON audit results with frame validation

---

### `vulture forensic device`

Run strong forensic device analysis against an offline capture.

```bash
vulture forensic device \
  --input capture.npz \
  --case-id C-005 \
  --subject device-01 \
  --frequency-hz 433920000
```

**Options:**
- `--input` (required): `.npz` or `.iq` capture file
- `--case-id` (required): Case identifier
- `--subject` (required): Subject identifier
- `--frequency-hz` (required): Center frequency in Hz
- `--output` (optional): File path
- `--format` (default: `json`): `json`, `txt`, or `html`

**Output:** Comprehensive device compromise analysis

---

### `vulture forensic report`

Write a forensic evidence report to disk in json/txt/html format.

```bash
vulture forensic report \
  --input capture.npz \
  --case-id C-005 \
  --subject device-01 \
  --frequency-hz 433920000 \
  --output forensic-report.json \
  --format json
```

**Options:**
- All options from `forensic device`
- `--output` (required): Output file path

**Output:** "✓ Report saved to [path]" with evidence hash

---

### `vulture forensic vulnerability`

Alias for device compromise analysis and vulnerability assessment.

```bash
vulture forensic vulnerability \
  --input capture.npz \
  --case-id C-005 \
  --subject device-01 \
  --frequency-hz 433920000
```

---

## Lab commands

### `vulture lab attack-sim`

Simulate an offensive scenario; no target, network, or transmitter is used.

```bash
vulture lab attack-sim --scenario spoofing --seed 7
```

**Options:**
- `--scenario` (required): `rf-jamming`, `spoofing`, `injection`, or `protocol-abuse`
- `--seed` (default: `7`): Random seed

**Output:** JSON with synthetic attack telemetry and evidence hash

---

### `vulture lab defense-sim`

Simulate detection and response against synthetic telemetry.

```bash
vulture lab defense-sim --scenario jamming-detection --seed 11
```

**Options:**
- `--scenario` (required): `jamming-detection`, `spoof-detection`, `protocol-anomaly`, or `chemical-rf-drift`
- `--seed` (default: `11`): Random seed

**Output:** JSON with detection results and evidence hash

---

## IQ commands

### `vulture iq convert`

Convert INPUT_PATH (.iq) to OUTPUT_PATH (.npz) with provenance metadata.

```bash
vulture iq convert capture.iq capture.npz \
  --source recorded_iq \
  --overwrite
```

**Arguments:**
- `INPUT_PATH` (required): Input `.iq` file
- `OUTPUT_PATH` (required): Output `.npz` file

**Options:**
- `--source` (default: `recorded_iq`): Source label
- `--overwrite` (flag): Replace existing file

**Output:** JSON with conversion metadata (SHA256, format, sample count)

---

## Offline commands

### `vulture offline analyze`

Analyze numeric values from a local whitespace/CSV file.

```bash
vulture offline analyze values.csv --sample-rate 1000000
```

**Arguments:**
- `PATH` (required): Input file path

**Options:**
- `--sample-rate` (optional): Sample rate in Hz

**Output:** JSON with statistical analysis (FFT, autocorrelation, moments, entropy)

---

## Quick reference

### Basic commands

```bash
vulture --help              # Show CLI tree
vulture info                # Display capabilities
vulture status              # Safe runtime status
vulture --interactive       # Enter interactive shell
```

### Chemical-RF science

```bash
vulture chemical-rf nmr --input capture.npz --nucleus 1H --field-t 7
vulture chemical-rf wavelength --frequency-hz 2.4e9
vulture chemical-rf path-loss --frequency-hz 2.4e9 --distance-m 10
```

### RF-DNA fingerprinting

```bash
vulture rf-dna simulate --profile multi-tone --duration 2 --output capture.npz
vulture rf-dna fingerprint --input capture.npz --label device-01
vulture rf-dna dashboard --input capture.npz
vulture rf-dna report --input capture.npz
vulture rf-dna quantum --profile multi-tone --duration 2
vulture rf-dna backends
vulture rf-dna status
```

### RF vulnerability assessment

```bash
vulture rf-vuln device --input capture.npz --case-id C-001 --subject dev-01 --frequency-hz 433920000
vulture rf-vuln report --input capture.npz --case-id C-001 --subject dev-01 --frequency-hz 433920000 --output report.json
```

### Forensic audits

```bash
vulture forensic physics --case-id C-001 --subject test --frequency-hz 2.4e9 --distance-m 10
vulture forensic chemistry --case-id C-002 --subject sample --compounds-json '[{"elements":{"H":2}}]'
vulture forensic math --case-id C-003 --subject sys --matrix-json '[[1,2],[3,4]]' --vector-json '[5,6]'
vulture forensic protocol --case-id C-004 --subject frame --frames-json '[{"length":4}]'
vulture forensic device --input capture.npz --case-id C-005 --subject dev --frequency-hz 433920000
vulture forensic report --input capture.npz --case-id C-005 --subject dev --frequency-hz 433920000 --output report.json
```

### Lab simulations

```bash
vulture lab attack-sim --scenario spoofing --seed 7
vulture lab defense-sim --scenario jamming-detection --seed 11
```

### IQ file operations

```bash
vulture iq convert capture.iq capture.npz --source recorded_iq --overwrite
```

### Offline analysis

```bash
vulture offline analyze values.csv --sample-rate 1000000
```

---

## File formats

All commands that accept capture files support:
- `.npz` - NumPy compressed archive (complex64 IQ + metadata)
- `.iq` - Binary complex64 little-endian (with optional `.iq.json` sidecar)

**Output formats:**
- `json` - JSON serialization (default)
- `txt` - Plain text report
- `html` - HTML page (forensic commands only)

---

## Evidence preservation

All commands generate:
- **SHA256 hash** for evidence chain of custody
- **ISO 8601 timestamps** in UTC
- **Case-linked metadata** for forensic tracking

---

## Safety guarantees

✅ **Receive-only** — No RF transmission  
✅ **Offline-only** — No network access  
✅ **Hardware-safe** — No automatic device access  
✅ **Local analysis** — All computation on user's machine  
✅ **Evidence-preserving** — SHA256 hashing for all operations  
✅ **Deterministic** — Reproducible results with seeds  

---

Last updated: 2026-10-09  
Version: 2.0+  
License: See LICENSE file
