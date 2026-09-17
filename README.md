# 🦅 VULTURE — Autonomous Intelligence & Research Platform

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue)](LICENSE)
[![RF](https://img.shields.io/badge/RF%20DNA-receive%20only-0A7B5E)](#rf-dna)

VULTURE is a modular scientific and RF research platform for reproducible analysis, SDR receive workflows, signal processing, machine learning, RF fingerprinting, and auditable evidence review. It provides a terminal interface, Python APIs, and a graphical interface where available.

> **Important:** VULTURE is designed for lawful, authorized research and defensive monitoring. RF-DNA and SDR integrations are receive/analyse-only by design. The project does not implement jamming, spoofing, unauthorized interception, credential theft, exploitation, or automatic transmission.

## What was restored and improved

The original VULTURE direction—RF intelligence, SDR/IQ processing, ML, fingerprinting, GUI, CLI, security, and scientific tooling—is restored here as the platform vision. The newer offline chemistry/physics/forensic workflows remain part of the project and are documented below. v3 adds a practical RF-DNA layer without pretending that optional hardware or cloud services are always available.

## Core capabilities

- **RF intelligence:** FFT, PSD, spectrograms, waterfall history, peak and burst detection, occupancy, noise-floor estimation, interference classification, and anomaly detection.
- **SDR/IQ workflows:** explicit device discovery, receive-only capture, IQ recording/playback, SigMF/NPY/BIN/WAV handling, metadata, calibration, resampling, and analysis pipelines.
- **RF-DNA fingerprinting:** reproducible feature extraction from supplied IQ, enrollment, similarity comparison, confidence scoring, dataset provenance, and signed audit records.
- **No-SDR mode:** deterministic IQ simulation, recorded-capture playback, synthetic test profiles, and offline benchmarking.
- **Remote RF-DNA:** optional authenticated service architecture for sending analysis jobs or receiving authorised IQ streams over TLS. Remote mode is disabled until explicitly configured and never discovers arbitrary networks.
- **CLI + GUI parity:** analysis commands are scriptable from the terminal and exposed through a PyQt6 dashboard where supported.
- **AI/ML:** classical ML, optional deep learning, model evaluation, explainable feature reports, and human approval before any automated action.
- **Scientific modules:** chemistry/RF calculations, spectroscopy, material screening, mathematical validation, and offline forensic reporting.
- **Quantum mechanics research:** optional quantum-signal-processing experiments such as QFT comparisons, variational classifiers, and noise-model studies. These are research features, not claims of quantum advantage.
- **Security:** RBAC, plugin permissions, input validation, encrypted local stores where configured, audit logs, HMAC-signed records, rate limiting, and fail-closed remote controls.

## RF-DNA

RF-DNA means **RF Distributed Networked Analysis** in this project: a controlled way to connect local analysis, approved remote receivers, simulators, and fingerprint databases. It is not a surveillance network and it does not enable unauthorized access.

### RF-DNA modes

| Mode | Hardware | Network | Purpose |
|---|---:|---:|---|
| `simulator` | No | No | Test pipelines with deterministic IQ |
| `file` | No | No | Analyse recorded IQ/SigMF evidence |
| `local-sdr` | Optional | No | Receive from an attached, authorized SDR |
| `remote-receiver` | Remote | TLS only | Consume an explicitly configured receiver |
| `service` | Optional | TLS only | Share approved analysis jobs and results |

### Supported design targets

- RTL-SDR, PlutoSDR, UHD/USRP, and SoapySDR-compatible receive devices when their vendor drivers are installed.
- Local simulator profiles: noise, CW, FM-like test signal, chirp, burst, QPSK-like samples, and multi-tone fixtures.
- Transport abstraction for future RF-DNA services; no hard-coded credentials or open Internet probing.
- Bounded sample rates, maximum capture durations, queue limits, and cancellation support.
- Dataset manifests containing timestamp, centre frequency, sample rate, gain, source, hash, and consent/authorization metadata.

### Safe receive-only examples

```bash
# Run a deterministic signal fixture without an SDR
python -m vulture.rf_dna.cli simulate --profile multi-tone --duration 2 --sample-rate 1000000 --output capture.npz

# Analyse a local capture
python -m vulture.rf_dna.cli fingerprint --input capture.npz --label lab-device-01

# Inspect configured receive backends; this does not open or transmit
python -m vulture.rf_dna.cli backends
```

The command module is intentionally separate from the legacy CLI until the project’s packaging and hardware-driver policy is finalised.

## Defensive and authorized research features

- Spectrum occupancy and interference alerts for owned/authorized bands.
- Baseline comparison and change detection.
- RF-DNA drift monitoring to detect hardware changes or replay-like differences in controlled datasets.
- Capture integrity hashes and chain-of-custody manifests.
- Explainable alerts with thresholds, evidence windows, and confidence—not opaque claims.
- Incident export to JSON/CSV/PDF-ready data for a human analyst.
- Prometheus-compatible metrics can be added by deployments without exposing IQ data.
- Safe lab exercises using simulators and prerecorded captures.

VULTURE does **not** provide offensive RF capabilities such as jamming, denial of service, spoofing, unauthorized interception, evasion, or attack automation. Defensive research can be powerful without adding those unsafe capabilities.

## Project structure

```text
VULTURE/
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/vulture/
│   ├── cli.py                         # Main Click CLI
│   ├── gui.py                         # Optional PyQt6 interface
│   ├── core/                          # Registry, configuration, permissions, audit
│   ├── rf_intelligence/               # FFT, PSD, spectrograms, detection
│   ├── sdr_iq_framework/              # IQ formats and device abstractions
│   ├── signal_processing/             # DSP and optional GPU acceleration
│   ├── ml_framework/                  # Training, evaluation, model persistence
│   ├── rf_fingerprinting_framework/   # Existing fingerprinting components
│   ├── rf_dna/                        # v3 simulator, fingerprints, safe SDR adapter
│   │   ├── __init__.py
│   │   ├── simulator.py
│   │   ├── fingerprint.py
│   │   ├── sdr_adapter.py
│   │   └── cli.py
│   ├── chemical_rf/                   # Chemistry/RF and spectroscopy
│   ├── forensics.py                   # Offline evidence audits
│   └── ...
├── tests/
├── docs/
└── rf_fingerprinting/
```

## Installation

```bash
git clone https://github.com/black-210/VULTURE.git
cd VULTURE
python -m pip install -e .
```

Optional development tools:

```bash
python -m pip install -e ".[dev]"
pytest -q
```

Optional SDR drivers are installed separately according to the hardware vendor and operating system. VULTURE must remain usable without them.

## CLI

Existing scientific and forensic commands remain available:

```bash
vulture info
vulture status
vulture rf-wavelength --frequency-hz 1e9
vulture rf-path-loss --frequency-hz 2.4e9 --distance-m 10
vulture chemical-rf nmr --nucleus 1H --field-t 7
vulture forensic physics --case-id C-001 --subject capture --frequency-hz 2.4e9 --distance-m 10
vulture --interactive
```

v3 RF-DNA utilities:

```bash
python -m vulture.rf_dna.cli --help
python -m vulture.rf_dna.cli simulate --profile noise --duration 1 --sample-rate 1000000 --output noise.npz
python -m vulture.rf_dna.cli fingerprint --input noise.npz --label test-fixture
python -m vulture.rf_dna.cli backends
```

All outputs should be treated as research results requiring review. A fingerprint is a statistical similarity result, not proof of identity.

## Offline scientific modules

The platform retains the chemistry, physics, mathematics, spectroscopy, material screening, and forensic audit workflows from the offline scientific edition. They are deterministic where possible, provenance-aware, and operate on explicit user input. No command silently opens hardware, scans a network, or transmits RF.

## Quantum mechanics / quantum signal processing

The optional QSP layer is intended for education and research:

- Quantum Fourier Transform versus classical FFT benchmarks.
- Variational quantum circuits for small RF feature vectors.
- Simulated quantum noise and robustness experiments.
- Hybrid classical/quantum model notebooks when Qiskit, Cirq, or another supported SDK is installed.
- Reproducible seeds, circuit diagrams, resource counts, and a classical baseline for every experiment.

Quantum features are optional and must not be required for ordinary RF analysis.

## Security model

- Explicit device allowlists; no arbitrary device or network discovery.
- Receive-only adapter contract; no transmit method is exposed by the v3 adapter.
- TLS and authentication are required for remote deployments.
- Per-job authorization, bounded resources, cancellation, and audit events.
- Plugin isolation and permission checks.
- SHA-256 capture hashes and provenance manifests.
- Human approval for exports, sharing, or any future hardware-control extension.

## Testing

```bash
pytest -q
pytest --cov=src --cov-report=term-missing
```

The RF-DNA modules include deterministic simulator and fingerprint tests. Hardware tests should run only in a controlled lab and must be marked separately from the offline test suite.

## Legal and ethical use

Use VULTURE only with systems, frequencies, datasets, and receivers you own or are explicitly authorized to test. Follow local spectrum rules, privacy laws, licensing requirements, and organizational policy. Do not use RF-DNA to identify people, track private devices, or intercept communications without lawful authorization.

## License

This project is distributed under the Apache 2.0 license unless otherwise noted. See `LICENSE`.

## Roadmap

- [x] Restore the original RF/SDR/AI/ML platform direction in the main README.
- [x] Add no-hardware RF-DNA simulation and reproducible fingerprinting primitives.
- [x] Add a receive-only SDR adapter boundary.
- [ ] Add an authenticated TLS RF-DNA service with tenant isolation.
- [ ] Add GUI RF-DNA dashboard and capture provenance viewer.
- [ ] Add optional SoapySDR/UHD integration tests for approved lab hardware.
- [ ] Add quantum experiment examples with classical baselines.

**VULTURE: powerful scientific and defensive analysis, explicit controls, and no unsafe automation.**
