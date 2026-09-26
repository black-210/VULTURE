# 🦅 VULTURE — Offline RF, Chemistry, Physics, Mathematics & Forensic Audit CLI

VULTURE is a comprehensive, receive-only RF analysis, fingerprinting, forensics, and physics toolkit designed for **authorized, local, offline analysis only**. It integrates chemical spectroscopy, electromagnetic physics, RF-DNA fingerprinting, forensic audit capabilities, and laboratory simulations into a unified CLI and Python API.

## Table of Contents
1. [Core Architecture](#core-architecture)
2. [Installation & Setup](#installation--setup)
3. [CLI Commands](#cli-commands)
4. [Python Library API](#python-library-api)
5. [File Format Support](#file-format-support)
6. [Module Reference](#module-reference)
7. [C Implementation](#c-implementation)
8. [Interactive Shell](#interactive-shell)
9. [Examples](#examples)

---

## Core Architecture

### Design Philosophy
- **Offline-first**: No network access, no hardware probing, no RF transmission
- **Evidence-based**: Every operation is auditable, with provenance tracking
- **Multi-format**: Supports canonical `.iq` (complex64 little-endian) and `.npz` (NumPy archive) capture formats
- **Modular**: Independent submodules for chemistry, RF analysis, forensics, physics, and ML
- **Safe by default**: Runtime status explicitly reports disabled hardware/network/transmission

### Top-Level Architecture

```
vulture/
├── cli.py                    # Main entry point, command routing
├── lab_cli.py               # Authorized laboratory simulations
├── forensic_cli.py          # Forensic audit commands
├── iq_cli.py                # IQ file conversion utilities
├── offline_tools/           # Standalone offline analysis
│   ├── cli.py
│   ├── workflow.py          # Analysis pipeline
│   ├── loaders.py           # CSV/text file loading
│   ├── stats.py             # Statistical analysis
│   └── validation.py        # Data validation
├── chemical_rf/             # Chemistry & RF science
│   ├── cli.py               # Chemical-RF commands
│   ├── science.py           # Wavelength, path loss
│   ├── spectroscopy.py      # Larmor frequency, NMR
│   ├── materials.py         # Permittivity, resonance
│   ├── pipeline.py          # Analysis workflow
│   └── calibration.py       # Impedance calibration
├── rf_dna/                  # RF fingerprinting & DNA analysis
│   ├── cli.py               # RF-DNA commands
│   ├── simulator.py         # Synthetic IQ generation
│   ├── fingerprint.py       # Fingerprint extraction
│   ├── dashboard.py         # Provenance dashboard
│   ├── reporting.py         # Report generation
│   ├── service.py           # Service layer
│   ├── sdr_adapter.py       # SDR abstraction (receive-only)
│   └── experiment_suite.py  # Quantum experiments
├── sdr_iq_framework/        # Canonical IQ file handling
│   ├── partition.py         # Binary IQ read/write
│   ├── convert.py           # IQ↔NPZ conversion
│   ├── iq_reader.py         # IQ parsing
│   ├── iq_writer.py         # IQ serialization
│   ├── integrity.py         # Checksum & validation
│   ├── capture_manifest.py  # Provenance metadata
│   └── commands.py          # High-level operations
├── forensics/               # Forensic audit framework
│   ├── __init__.py          # Public audit API
│   └── (physics, chemistry, math, protocol auditors)
├── lab/                     # Red-team/blue-team simulations
│   └── __init__.py          # attack_simulation, defense_simulation
├── rf_dna/                  # (See above)
├── rf_fingerprinting_framework/  # ML-based RF fingerprinting
│   ├── feature_extraction.py     # Extract RF features
│   ├── classification.py         # ML classifiers
│   ├── clustering.py             # Clustering algorithms
│   └── iq_analyzer.py            # IQ constellation analysis
├── ml_framework/            # ML training & evaluation
│   ├── model_trainer.py
│   ├── evaluation.py
│   └── feature_engineering.py
└── visualization_advanced/  # Advanced visualization
    ├── iq_constellation.py  # IQ plots
    ├── spectrum_viewer.py   # Frequency domain
    └── waterfall_3d.py      # 3D spectrograms
```

---

## Installation & Setup

### From Source
```bash
python -m pip install -e .
python -m pip install -e ".[dev]"      # Development dependencies
python -m pip install -e ".[science]"  # scipy, pandas, matplotlib
python -m pip install -e ".[ml]"       # scikit-learn, onnx
python -m pip install -e ".[security]" # cryptography, pydantic
```

### Verify Installation
```bash
vulture --help
vulture rf-dna --help
python -m vulture.rf_dna.cli --help
```

### C Binaries (Optional)
```bash
make -C c              # Build all C utilities
./vulture-c --help     # Main C CLI
./vulture_cli --help   # Direct CLI parser
./vulture-iq --help    # IQ file tools
```

---

## CLI Commands

### Main Command Groups

#### 1. **vulture info**
Displays platform capabilities and module availability.
```bash
vulture info
```
**Output**: Lists available science domains, forensics, RF-DNA, and interactive mode.

#### 2. **vulture status**
Reports safe runtime status; confirms offline mode, no hardware access, no network.
```bash
vulture status
```
**JSON Output**:
- `cli`: "online"
- `mode`: "offline-deterministic"
- `hardware`: "not-opened"
- `network`: "disabled"
- `rf_transmit`: "disabled"
- `analysis`: "local-only"
- `capture_formats`: ["npz", "iq"]

#### 3. **vulture chemical-rf** (Chemistry & RF Physics)

**NMR Calculation**:
```bash
# With NPZ capture:
vulture chemical-rf nmr --input capture.npz --nucleus 1H --field-t 7

# With IQ capture:
vulture chemical-rf nmr --input capture.iq --nucleus 1H --field-t 7

# Output: Larmor frequency in Hz, capture metadata
```

**Material Analysis**:
```bash
vulture chemical-rf material --input capture.npz \
  --epsilon-r 4.2 --conductivity 0.01 \
  --frequency-hz 2.4e9 --length-m 0.1

# Output: Complex permittivity (real/imag), resonance frequency
```

**RF Physics**:
```bash
vulture chemical-rf physics --input capture.npz \
  --frequency-hz 2.4e9 --distance-m 10

# Output: Wavelength (m), free-space path loss (dB)
```

**Impedance Report**:
```bash
vulture chemical-rf report --input capture.npz \
  --sample-id S-001 --real-ohm 50 --imag-ohm 2.5

# Output: Auditable impedance analysis with capture provenance
```

#### 4. **vulture rf-dna** (RF Fingerprinting & DNA Analysis)

**Status**:
```bash
vulture rf-dna status  # Capabilities, available backends
```

**Simulate** (Local IQ Generation):
```bash
vulture rf-dna simulate --profile multi-tone \
  --duration 2 --sample-rate 1000000 --seed 7 \
  --output capture.npz

# Profiles: "cw", "multi-tone", "fsk", "chirp", "noise"
```

**Fingerprint** (Extract RF Signature):
```bash
vulture rf-dna fingerprint --input capture.npz --label lab-device-01

# Output: Device fingerprint, digest, similarity metrics
```

**Dashboard** (Provenance Summary):
```bash
vulture rf-dna dashboard --input capture.npz --label capture-1

# Output: Capture metadata, RF summary, source tracking
```

**Report** (Machine-Readable Evidence):
```bash
vulture rf-dna report --input capture.npz --label report-001

# Output: Complete RF-DNA analysis, timestamps, evidence chain
```

**Quantum** (Quantum-Inspired Baseline):
```bash
vulture rf-dna quantum --profile multi-tone --duration 2 --seed 7

# Output: Classical RF baseline + quantum experiment results
```

**Backends** (Optional Receive Interfaces):
```bash
vulture rf-dna backends

# Output: SoapySDR availability, supported formats, offline mode confirmation
```

#### 5. **vulture forensic** (Offline Evidence Audit)

All forensic commands support optional `.npz`/`.iq` capture linking.

**Physics Audit**:
```bash
# Standalone (no capture):
vulture forensic physics --case-id C-001 --subject test \
  --frequency-hz 2.4e9 --distance-m 10 --bandwidth-hz 20e6

# With capture context:
vulture forensic physics --input capture.npz \
  --case-id C-001 --subject test \
  --frequency-hz 2.4e9 --distance-m 10
```

**Chemistry Audit**:
```bash
vulture forensic chemistry --input capture.npz \
  --case-id C-002 --subject sample \
  --compounds-json '[{"elements":{"H":2,"O":1}}]'

# Validates compound composition, checks for invalid values
```

**Mathematics Audit**:
```bash
vulture forensic math --input capture.iq \
  --case-id C-003 --subject system \
  --matrix-json '[[2,1],[1,1]]' --vector-json '[3,2]'

# Checks matrix dimensions, non-finite values, linear system plausibility
```

**Protocol Audit**:
```bash
vulture forensic protocol --input capture.npz \
  --case-id C-004 --subject frame \
  --frames-json '[{"length":4,"declared_length":4}]'

# Validates frame structure, protocol consistency
```

**Output Options**:
```bash
# JSON format (default):
--format json

# Text format:
--format txt

# Write to file:
--output audit-report.txt
```

#### 6. **vulture lab** (Authorized Simulations)

**Attack Simulation** (No Target/Network/Transmitter Used):
```bash
vulture lab attack-sim --scenario spoofing --seed 7

# Scenarios: "rf-jamming", "spoofing", "injection", "protocol-abuse"
# Output: Synthetic attack telemetry, SHA256 evidence hash
```

**Defense Simulation**:
```bash
vulture lab defense-sim --scenario jamming-detection --seed 11

# Scenarios: "jamming-detection", "spoof-detection", 
#            "protocol-anomaly", "chemical-rf-drift"
# Output: Detection results, automatic transmission disabled markers
```

#### 7. **vulture iq** (IQ File Operations)

**Convert .iq to .npz**:
```bash
vulture iq convert capture.iq capture.npz \
  --source recorded_iq --overwrite

# Preserves: complex64 samples, sample rate, provenance
```

#### 8. **vulture offline** (Standalone Analysis)

**Analyze CSV/Whitespace Data**:
```bash
vulture offline analyze values.csv --sample-rate 1000000

# Output: Statistical analysis, frequency domain features
```

#### 9. **vulture --interactive**

Launches friendly `>` prompt with local, offline commands.
```bash
vulture --interactive
> help           # Show all available commands
> status         # Display platform status
> chemical-rf nmr --input capture.npz --nucleus 1H --field-t 7
> forensic physics --case-id C-001 --subject test --frequency-hz 2.4e9 --distance-m 10
> history        # Show command history
> exit           # Close session safely
```

---

## Python Library API

### High-Level Chemistry API

```python
from vulture.chemical_rf.spectroscopy import larmor_frequency_hz
from vulture.chemical_rf.science import free_space_path_loss_db, wavelength_m
from vulture.chemical_rf.materials import complex_permittivity, dielectric_resonance_frequency

# Larmor frequency for 1H nucleus at 7T:
freq = larmor_frequency_hz("1H", 7.0)  # ~298 MHz

# RF physics:
wavelength = wavelength_m(2.4e9)  # ~0.125 m (2.4 GHz)
path_loss = free_space_path_loss_db(2.4e9, 10)  # dB at 10 m

# Material analysis:
epsilon = complex_permittivity(epsilon_r=4.2, conductivity=0.01, frequency_hz=2.4e9)
resonance = dielectric_resonance_frequency(epsilon_r=4.2, length_m=0.1)
```

### RF-DNA Fingerprinting API

```python
from vulture.rf_dna.simulator import generate_iq
from vulture.rf_dna.fingerprint import extract_fingerprint, similarity

# Generate deterministic IQ:
iq = generate_iq(profile="multi-tone", duration=0.01, sample_rate=10_000)

# Extract fingerprint:
fp = extract_fingerprint(iq, 10_000)  # Returns Fingerprint object
print(fp.digest)  # Unique identifier
print(fp.metrics)  # Statistical features

# Compare fingerprints:
sim = similarity(fp1, fp2)  # 0.0 (different) to 1.0 (identical)
```

### SDR IQ Framework

```python
from vulture.sdr_iq_framework.partition import read_iq_file, write_iq_file
from vulture.sdr_iq_framework.convert import convert_iq_to_npz
from vulture.sdr_iq_framework.integrity import sha256_file

# Read canonical .iq file:
samples, sample_rate = read_iq_file("capture.iq")

# Write IQ data:
write_iq_file("output.iq", samples, sample_rate)

# Convert to NPZ:
result = convert_iq_to_npz("capture.iq", "capture.npz", source="recorded_iq")
# Returns: {"input", "output", "source", "format", "sha256", "sample_count", "dtype"}

# Integrity check:
sha256 = sha256_file("capture.iq")
```

### Forensic Audit API

```python
from vulture.forensics import audit_physics, audit_chemistry, audit_mathematics, audit_protocol, write_report

# Physics audit:
report = audit_physics(
    case_id="C-001",
    subject="test",
    frequency_hz=2.4e9,
    distance_m=10,
    bandwidth_hz=20e6
)

# Chemistry audit:
compounds = [{"elements": {"H": 2, "O": 1}}]
report = audit_chemistry("C-002", "sample", compounds)

# Math audit:
matrix = [[2, 1], [1, 1]]
vector = [3, 2]
report = audit_mathematics("C-003", "system", matrix, vector)

# Protocol audit:
frames = [{"length": 4, "declared_length": 4}]
report = audit_protocol("C-004", "frame", frames)

# Write report to file:
write_report(report, "report.txt", fmt="txt")

# JSON/text output:
print(report.to_json())
print(report.to_text())
```

### Lab Simulations API

```python
from vulture.lab import attack_simulation, defense_simulation

# Attack simulation (no actual transmission):
result = attack_simulation(scenario="spoofing", seed=7)
print(result.to_dict())  # Synthetic attack telemetry

# Defense simulation:
result = defense_simulation(scenario="jamming-detection", seed=11)
print(result.to_dict())  # Detection results
```

### Offline Analysis Workflow

```python
from vulture.offline_tools.loaders import load_numbers
from vulture.offline_tools.workflow import analyze

# Load CSV/whitespace data:
numbers = load_numbers("data.csv")

# Analyze:
result = analyze(numbers, sample_rate=1_000_000)
# Returns: FFT, autocorrelation, moments, entropy
```

---

## File Format Support

### .iq Format (Canonical)
- **Binary Layout**: Little-endian complex64 (float32 I + float32 Q per sample)
- **Size**: 8 bytes per complex sample
- **Metadata**: JSON sidecar `.iq.json` with sample_rate, center_frequency, timestamp
- **Validation**: Must contain complete complex64 samples (size % 8 == 0)
- **Use Case**: Raw SDR captures, hardware recordings, long-term storage

**Example .iq.json Sidecar**:
```json
{
  "sample_rate": 1000000,
  "center_frequency": 2400000000,
  "timestamp": "2026-09-26T08:00:00Z",
  "duration_seconds": 1.5,
  "sample_count": 1500000
}
```

### .npz Format (NumPy Archive)
- **Binary Layout**: Compressed NumPy archive with named arrays
- **Keys**: `iq` (complex64), `sample_rate` (float), `source` (str), `format` (str), `sha256` (str)
- **Compression**: zlib (configurable)
- **Metadata**: Complete provenance including source, format, hash
- **Use Case**: Python analysis, quick processing, cloud storage

**Create NPZ Programmatically**:
```python
import numpy as np
np.savez_compressed(
    "capture.npz",
    iq=samples,
    sample_rate=1_000_000,
    source="recorded_iq",
    format="complex64-le",
    sha256="abc123...",
    sample_count=1_000_000,
    dtype="complex64"
)
```

### Format Conversion

```bash
# IQ → NPZ (recommended for Python analysis):
vulture iq convert capture.iq capture.npz

# NPZ → IQ (export for hardware):
python -c "
import numpy as np
data = np.load('capture.npz')
data['iq'].astype('complex64').tofile('output.iq')
"
```

---

## Module Reference

### vulture.chemical_rf.science
- `wavelength_m(frequency_hz)` — Calculate wavelength
- `free_space_path_loss_db(frequency_hz, distance_m)` — Friis formula
- Constants: speed of light, permittivity of free space

### vulture.chemical_rf.spectroscopy
- `larmor_frequency_hz(nucleus, field_tesla)` — NMR Larmor frequency
- Supported nuclei: 1H, 13C, 15N, 19F, 31P, etc.
- Constants: magnetogyric ratios for each nucleus

### vulture.chemical_rf.materials
- `complex_permittivity(epsilon_r, conductivity, frequency_hz)` — Debye model
- `dielectric_resonance_frequency(epsilon_r, length_m)` — Half-wave resonance
- Returns: Complex permittivity ε = ε' + j·ε''

### vulture.chemical_rf.pipeline
- `ChemicalRFAnalysisPipeline().analyze_impedance(sample_id, impedance_complex, metadata)` — Full analysis
- Input validation, uncertainty quantification
- Output: Auditable report with traces

### vulture.rf_dna.simulator
- `generate_iq(profile, duration, sample_rate, seed=None)` — Deterministic IQ generation
- Profiles: "cw" (sine wave), "multi-tone", "fsk", "chirp", "noise"
- Returns: NumPy complex64 array

### vulture.rf_dna.fingerprint
- `extract_fingerprint(iq_samples, sample_rate)` — Extract RF signature
- Metrics: crest factor, PAR, spectral flatness, entropy
- `similarity(fp1, fp2)` — Compare fingerprints (0.0 to 1.0)

### vulture.rf_dna.dashboard
- `build_capture_from_npz(path, label)` — Load capture metadata
- `build_dashboard_summary(captures)` — Generate dashboard JSON
- Includes: Timestamp, sample count, source, provenance chain

### vulture.rf_dna.reporting
- `generate_report(input_path, label)` — Create machine-readable report
- JSON format with full RF-DNA analysis
- Includes: Fingerprint, device signature, uncertainty

### vulture.sdr_iq_framework.partition
- `read_iq_file(path, sample_rate=None)` — Load .iq with sidecar
- `write_iq_file(path, samples, sample_rate)` — Save .iq + .json
- Validation: Checks completeness, endianness, finiteness

### vulture.sdr_iq_framework.convert
- `convert_iq_to_npz(input_path, output_path, source="recorded_iq", overwrite=False)` — Full conversion
- Preserves: Samples, sample rate, provenance, integrity hash
- Output: NPZ-ready for Python pipeline

### vulture.sdr_iq_framework.integrity
- `sha256_file(path, chunk_size=1<<20)` — Streaming SHA256
- `iq_byte_count(path)` — Validate byte alignment (must be divisible by 8)

### vulture.sdr_iq_framework.capture_manifest
- Provenance metadata: Timestamp, source, authorization
- Tenant scoping for multi-user deployments
- Verification against tamper-resistant records

### vulture.forensics (Audit Framework)
- `audit_physics(case_id, subject, frequency_hz, distance_m, bandwidth_hz=None)` — Plausibility check
- `audit_chemistry(case_id, subject, compounds)` — Composition validation
- `audit_mathematics(case_id, subject, matrix, vector)` — Linear system audit
- `audit_protocol(case_id, subject, frames)` — Frame structure validation
- `write_report(report, path, fmt)` — Save to file (txt or JSON)
- All return: `.to_json()`, `.to_text()` formatted output

### vulture.lab
- `attack_simulation(scenario, seed)` — Synthetic offensive scenario
- `defense_simulation(scenario, seed)` — Synthetic detection scenario
- Returns: Auditable result object with SHA256 evidence hash

### vulture.offline_tools
- `load_numbers(path)` — Parse CSV/whitespace numeric data
- `analyze(numbers, sample_rate)` — Statistical + FFT analysis
- Returns: Mean, std, min, max, FFT peaks, autocorrelation, entropy

### vulture.rf_fingerprinting_framework
- `IQAnalyzer.compute_iq_imbalance(signal)` — Amplitude/phase imbalance metrics
- `IQAnalyzer.compute_constellation_metrics(signal)` — EVM, radius statistics
- ML feature extraction for classification models

---

## C Implementation

The C layer provides low-level, high-performance RF analysis and direct hardware abstraction.

### Compilation
```bash
make -C c                    # Build all C utilities
make -C c clean              # Remove build artifacts
make -C c vulture-c          # Just main binary
make -C c vulture-iq         # Just IQ binary
make -C c vulture_cli        # Just CLI parser
```

### C Binaries

#### vulture-c (Main C CLI)
```bash
./vulture-c --help
./vulture-c analyze capture.iq
./vulture-c status           # SDR status
./vulture-c --version
```
**Features**:
- Direct binary IQ parsing (no Python overhead)
- Streaming FFT for large files
- Peak detection, spectral analysis
- SDR device enumeration (SoapySDR backend)

#### vulture-iq (IQ File Tools)
```bash
./vulture-iq iq validate capture.iq
./vulture-iq iq stats capture.iq --sample-rate 1000000
./vulture-iq sdr status
```
**Operations**:
- `iq validate` — Check format, completeness, finiteness
- `iq stats` — Sample count, duration, I/Q means, RMS, peak, crest factor, phase, zero-crossing rate
- `sdr status` — Report safe runtime boundary

#### vulture_cli (Direct Parser)
Direct command-line parsing without routing through Python Click.
```bash
./vulture_cli help
./vulture_cli nmr 1H 7.0     # Larmor frequency
./vulture_cli path-loss 2.4e9 10  # Free-space path loss
```

### C Code Structure
```
c/
├── vulture_c.c              # Main entry point
├── vulture_c_features.c     # Feature extraction
├── vulture_cli.c            # CLI parser
├── vulture_iq.c             # IQ file operations
├── vulture_iq_*.c           # Specialized IQ analysis (balance, correlation, phase, etc.)
├── vulture_core.c/.h        # Core utilities, error handling
├── vulture_sdr.c/.h         # SDR abstraction (SoapySDR wrapper)
├── vulture_iq_reader.c/.h   # IQ binary parsing
├── vulture_iq_partition.c/.h # File partitioning, streaming
├── vulture_hash_engine.c    # SHA256 integrity
├── vulture_rf_analysis.c    # RF feature computation
├── engines/                 # Pluggable analysis engines
│   ├── vulture_hash_engine.c
│   └── vulture_rf_analysis.c
├── translator/
│   └── vulture_tool_translator.c  # Tool invocation layer
├── Makefile                 # Build rules
├── IQ_CLI_TARGET.mk         # IQ-specific targets
├── IQ_FEATURES.mk           # Feature flags
└── README.md                # C layer documentation
```

### Key C Functions

**IQ Reading** (`vulture_iq_reader.c`):
```c
int read_iq_file_le(const char *path, complex_float *buffer, 
                    size_t max_samples, size_t *out_count);
// Reads little-endian complex64 .iq file
// Returns: 0 success, -1 file error, -2 format error
```

**IQ Statistics** (`vulture_iq_stats.c`):
```c
struct iq_stats compute_iq_stats(const complex_float *iq, size_t count);
// Computes: mean, rms, peak, power, crest factor, zero-crossing rate
struct {
    float mean_i, mean_q;
    float rms_i, rms_q;
    float peak_i, peak_q;
    float mean_power;
    float crest_factor;
    float zcr;  // zero-crossing rate
};
```

**Spectral Analysis** (`vulture_iq_spectrum.c`):
```c
struct spectrum compute_spectrum(const complex_float *iq, size_t count,
                                 int fft_size, enum window_type window);
// Windowed FFT (Hamming, Hann, Blackman, etc.)
// Returns: power spectral density, peak frequencies
```

**SDR Interface** (`vulture_sdr.c`):
```c
struct sdr_device *sdr_open(const char *device_args, size_t sample_rate);
int sdr_read_samples(struct sdr_device *dev, complex_float *buffer, 
                     size_t count, int timeout_ms);
// Wraps SoapySDR, handles errors, reports timeout/overflow
```

**Integrity** (`vulture_hash_engine.c`):
```c
void sha256_file(const char *path, unsigned char digest[32]);
// Streaming SHA256 of binary .iq file
// Used for provenance chain validation
```

### C Build Flags
```makefile
# In c/Makefile:
CFLAGS += -O3 -Wall -Wextra -std=c99
CFLAGS += -fPIC                         # Position-independent code
CFLAGS += -DUSE_SOAPYSDR                # Include SDR support (optional)
CFLAGS += -DENABLE_STREAMING            # Streaming mode for large files
LDFLAGS += -lm                          # Math library
LDFLAGS += -lSoapySDR                   # SDR library (if enabled)
```

### Integration with Python
Python modules call C binaries via subprocess, or link C libraries via ctypes:
```python
import ctypes
libvulture = ctypes.CDLL('./c/libvulture.so')

# Directly invoke C function
iq_stats = libvulture.compute_iq_stats(buffer, count)
```

---

## Interactive Shell

The interactive shell (`vulture --interactive`) provides a friendly `>` prompt for experimenting with commands without shell escaping or subprocess overhead.

### Shell Features

**Auto-Discovery**: Lists all available commands (chemical-rf, rf-dna, forensic, lab, etc.)

**History**: `history` command recalls previous commands with numeric indices

**Help**: Built-in `help` or `?` displays command syntax and examples

**Direct Execution**: Commands are routed to Click CLI internally without spawning new processes

**Error Handling**: Graceful exception catching; invalid commands don't crash the shell

### Example Interactive Session
```
══════════════════════════════════════════════════════════
🦅 VULTURE — Offline Scientific Intelligence Platform
Supports .iq and .npz • chemistry • physics • forensics
Type: help | status | forensic physics | exit
══════════════════════════════════════════════════════════

> status
{
  "analysis": "local-only",
  "cli": "online",
  ...
}

> chemical-rf nmr --input capture.npz --nucleus 1H --field-t 7
{
  "captured_sample_rate": 1000000.0,
  "frequency_hz": 298000000.0,
  "nucleus": "1H",
  ...
}

> forensic physics --case-id C-001 --subject test --frequency-hz 2.4e9 --distance-m 10
{
  "case_id": "C-001",
  "plausibility": "valid",
  ...
}

> history
1: status
2: chemical-rf nmr --input capture.npz --nucleus 1H --field-t 7
3: forensic physics --case-id C-001 --subject test --frequency-hz 2.4e9 --distance-m 10

> exit
✓ Session closed safely.
```

### Implementation (`vulture/cli.py`)
```python
class InteractiveShell:
    def __init__(self):
        self.running = True
        self.history = []
    
    def run(self):
        self.banner()
        while self.running:
            try:
                cmd = click.prompt(">", prompt_suffix=" ")
            except (EOFError, KeyboardInterrupt):
                break
            self.process(cmd)
    
    def process(self, line: str):
        line = line.strip()
        if not line:
            return
        self.history.append(line)
        
        # Route to CLI
        try:
            cli.main(shlex.split(line), standalone_mode=False)
        except SystemExit:
            pass
        except Exception as exc:
            click.echo(f"error: {exc}")
```

---

## Examples

### Example 1: Simulate RF Capture → Fingerprint → Audit

```bash
# Step 1: Generate synthetic IQ
vulture rf-dna simulate --profile multi-tone --duration 1 \
  --sample-rate 1000000 --output test.npz

# Step 2: Extract fingerprint
vulture rf-dna fingerprint --input test.npz --label device-001

# Step 3: Forensic physics audit
vulture forensic physics --input test.npz \
  --case-id C-001 --subject device-001 \
  --frequency-hz 2.4e9 --distance-m 5

# Step 4: Generate report
vulture rf-dna report --input test.npz --label report-001
```

### Example 2: IQ File Conversion → Chemical Analysis

```bash
# Assume we have raw capture with sidecar:
# capture.iq (binary)
# capture.iq.json ({"sample_rate": 1000000, "center_frequency": 2.4e9})

# Convert to NPZ
vulture iq convert capture.iq capture.npz --overwrite

# Run chemistry analysis
vulture chemical-rf material --input capture.npz \
  --epsilon-r 4.2 --frequency-hz 2.4e9 --length-m 0.05

# Run physics calculation
vulture chemical-rf physics --input capture.iq \
  --frequency-hz 2.4e9 --distance-m 8
```

### Example 3: Forensic Audit with Multiple Evidence Types

```bash
# Physics audit
vulture forensic physics --input capture.npz \
  --case-id CASE-2026-001 --subject RF-capture \
  --frequency-hz 2.4e9 --distance-m 10 --bandwidth-hz 20e6 \
  --format json --output case-physics.json

# Chemistry audit
vulture forensic chemistry --input capture.npz \
  --case-id CASE-2026-001 --subject sample-A \
  --compounds-json '[{"elements":{"H":2,"C":1,"O":1}}]' \
  --format txt --output case-chemistry.txt

# Math audit
vulture forensic math --case-id CASE-2026-001 --subject system-params \
  --matrix-json '[[1,2],[3,4]]' --vector-json '[5,6]' \
  --format json --output case-math.json

# All reports now linked to same capture via --input
```

### Example 4: Laboratory Simulation (No Transmission)

```bash
# Simulate attack scenario
vulture lab attack-sim --scenario spoofing --seed 42

# Output includes:
# - attack_type: "spoofing"
# - synthetic_signal_power: X dBm
# - evidence_sha256: "abc123..."
# - authorization: "APPROVED_OFFLINE_LAB"
# - transmission_status: "disabled"

# Simulate defense
vulture lab defense-sim --scenario jamming-detection --seed 42

# Output includes:
# - detection_result: true/false
# - confidence: 0.0-1.0
# - evidence_sha256: "def456..."
```

### Example 5: Python API Usage

```python
import numpy as np
from vulture.sdr_iq_framework.convert import convert_iq_to_npz
from vulture.chemical_rf.spectroscopy import larmor_frequency_hz
from vulture.rf_dna.fingerprint import extract_fingerprint

# Convert IQ to NPZ
result = convert_iq_to_npz("raw.iq", "processed.npz", source="lab-capture")
print(f"SHA256: {result['sha256']}")

# Load NPZ
data = np.load("processed.npz")
iq_samples = data["iq"]
sample_rate = float(data["sample_rate"])

# Fingerprint analysis
fp = extract_fingerprint(iq_samples, sample_rate)
print(f"Device ID: {fp.digest}")
print(f"Crest Factor: {fp.metrics['crest_factor']:.2f}")

# NMR calculation
larmor = larmor_frequency_hz("1H", 3.0)  # 3T field
print(f"Larmor Frequency: {larmor / 1e6:.1f} MHz")
```

---

## Module Dependencies & Loops

### Core Dependencies
- **Click**: CLI framework, command routing, option parsing
- **NumPy**: Array operations, FFT, statistics
- **SciPy** (optional): Signal processing, special functions
- **scikit-learn** (optional): ML classification, clustering
- **matplotlib** (optional): Visualization

### Main Processing Loops

**RF-DNA Fingerprinting Loop**:
```python
for profile in profiles:
    iq = generate_iq(profile, duration, sample_rate)
    fp = extract_fingerprint(iq, sample_rate)
    for existing_fp in database:
        score = similarity(fp, existing_fp)
        if score > threshold:
            match(profile, existing_fp)
```

**Forensic Audit Loop**:
```python
for case in cases:
    for subject in case.subjects:
        report = audit_physics(case.id, subject.name, ...)
        if report.is_valid:
            write_report(report, output_path)
        else:
            flag_anomaly(case.id, subject.name)
```

**Interactive Shell Loop**:
```python
while running:
    cmd = prompt("> ")
    try:
        cli.main(parse(cmd))
    except Exception as e:
        echo(f"error: {e}")
```

---

## Safety & Guarantees

### Offline-Only Verification
- No network calls (except SoapySDR optional hardware detection)
- No persistent state shared across sessions
- No external service dependencies
- All data remains on local disk

### Integrity Guarantees
- SHA256 hashing of all input files
- Provenance metadata in every report
- Tamper detection via cryptographic verification
- Evidence chain tracking through case IDs

### Hardware Boundaries
- SDR devices opened in **receive-only mode**
- TX (transmit) explicitly disabled by default
- Status command reports "rf_transmit": "disabled"
- Lab simulations use only synthetic data

---

## Summary

VULTURE integrates chemistry, RF physics, signal analysis, and forensic audit into a unified platform. Its **multi-format support** (`.npz`, `.iq`), **comprehensive Python API**, **performant C layer**, and **interactive shell** make it ideal for authorized offline RF analysis, device fingerprinting, evidence auditing, and laboratory simulation. All operations preserve provenance, maintain offline safety, and report clear status indicators.

For questions or contributions, see the repository documentation and test suite.
