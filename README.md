# VULTURE 🦅 — Unified RF, SDR, DSP & AI Toolkit

[![CI](https://github.com/black-210/VULTURE/actions/workflows/ci.yml/badge.svg)](https://github.com/black-210/VULTURE/actions/workflows/ci.yml)
[![Quality](https://github.com/black-210/VULTURE/actions/workflows/quality.yml/badge.svg)](https://github.com/black-210/VULTURE/actions/workflows/quality.yml)

This README is the authoritative, up-to-date main document for the VULTURE repository. It lists every framework, the implementation readiness status, where code lives, how to run things locally, and the immediate next work required to reach production readiness.

Contents
- Quick status matrix
- How to use this repo (checkout, tests, CLI)
- Per-framework details (purpose, files, readiness, next steps)
- Roadmap & priority list
- Contributing, CI, and contacts

---

Quick status matrix (truthful readiness)

Legend: Ready = usable end-to-end; Partial = working stubs + some implementations; Scaffold = interfaces & placeholders (needs implementation)

| Framework | Status | Notes |
|---|---:|---|
| CORE ENGINE | Partial (scaffolded) | Core entrypoint, config, logging, simple run() — DI/Registry/Policy need expansion |
| AI Intelligence | Scaffold | LLM adapter stubs, vision adapter placeholders, codegen/tool-executor interfaces |
| RF Intelligence | Partial | FFT (numpy) + anomaly wrapper implemented; PSD/spectrogram/peak/burst still placeholders |
| SDR / IQ Framework | Scaffold | Hardware interface, record/playback stubs, format detection/metadata |
| Signal Processing (DSP) | Partial | FFT + window functions implemented; filters/synchronization/optimized GPU pipelines TODO |
| ML / Deep Learning | Partial | Preprocessing, Trainer wrapper (sklearn), PyTorch helpers implemented as utilities |
| RF Fingerprinting | Partial | Basic feature extraction + clustering/classifier wrappers implemented |
| Spectrum Intelligence | Scaffold | Analyzer & visualizer stubs — visualization and monitoring logic TODO |
| Physics Laboratory | Partial | Antenna & LinkBudget implemented; propagation models TODO |
| Dataset Intelligence | Partial | CSV/JSON/NPY/Parquet loaders + validation & transforms (fallbacks) |
| Plugin Framework | Scaffold | Discovery/permission/sandbox stubs |
| Model Hub | Scaffold | Local repo + ONNX loader stubs |
| CLI Interface | Partial | CLI skeleton & parse_args — subcommands placeholders |
| PyQt6 GUI | Scaffold | Multi-tab GUI scaffold (not wired to backends)

---

How to use this repository locally

1) Clone & checkout working branch (feature/add-scaffold)

```bash
git clone https://github.com/black-210/VULTURE.git
cd VULTURE
git fetch origin
git checkout feature/add-scaffold
```

2) Recommended: create virtualenv and install dev deps

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pytest numpy pandas scikit-learn
```

3) Run unit tests (they use fallbacks when heavy libs are absent)

```bash
pytest -q
```

4) Try CLI entrypoint

```bash
python -m vulture.main --help
python -m vulture.main --verbose
```

---

Per-framework detail (files, readiness, next steps)

Note: links point to the feature/add-scaffold branch for quick navigation.

1) CORE ENGINE — vulture/*
- Files: `vulture/__init__.py`, `vulture/main.py`, `vulture/cli.py`, `vulture/config.py`, `vulture/utils.py`, `vulture/services.py`
- Status: Partial (scaffold + working runner)
- Purpose: package metadata, CLI parsing, config loading, logging and a top-level run() function.
- Next Steps: Add a DI container, framework registry, plugin manager integration, policies and role-based permissions.
- Browse: https://github.com/black-210/VULTURE/tree/feature%2Fadd-scaffold/vulture

2) AI INTELLIGENCE FRAMEWORK — vulture/ai (scaffolded)
- Files: (adapter stubs are scaffolded in repo under AI folders / placeholders)
- Status: Scaffold
- Purpose: Route to LLM providers (OpenAI, local), vision model adapter (CLIP), tool executor sandbox interface.
- Next Steps: Implement concrete adapters, credentials handling, rate-limiting, secure tool execution.

3) RF INTELLIGENCE FRAMEWORK — vulture/dsp & vulture/rf (partial)
- Files: `vulture/dsp/*`, PSD & spectrogram placeholders, FFT wrapper in `vulture/dsp/fft.py`.
- Status: Partial
- Purpose: Spectrum analysis building blocks (FFT, PSD, spectrogram, peak detection, occupancy, burst detection).
- Next Steps: Implement Welch/Multitaper PSD (scipy.signal), spectrogram using scipy or matplotlib, peak detection (CWT/prominence), occupancy analysis.

4) SDR / IQ FRAMEWORK — vulture/sdr/*
- Files: `vulture/sdr/hardware.py`, `vulture/sdr/iqio.py`, `vulture/sdr/format.py`, `vulture/sdr/metadata.py`
- Status: Scaffold
- Purpose: Abstract hardware drivers; record/playback; format detection; metadata extraction (SigMF sidecars support planned).
- Next Steps: Implement concrete drivers (pyrtlsdr, uhd, libiio/pluto), robust error handling and unit tests with hardware mocks.

5) SIGNAL PROCESSING FRAMEWORK — vulture/dsp/*
- Files: `fft.py`, `psd.py`, `spectrogram.py`, `filters.py`, `window.py`
- Status: Partial
- Purpose: Core DSP ops — FFT/IFTT, PSD, spectrogram, windowing, filters, GPU acceleration detection.
- Next Steps: Implement SciPy-backed PSD/spectrogram, filter design with scipy.signal (butter, filtfilt), numba/CuPy speedups.

6) ML / Deep Learning — vulture/ml/*
- Files: `preprocess.py`, `features.py`, `training.py`, `validation.py`, `pytorch.py`, `gpu.py`
- Status: Partial
- Purpose: Preprocessing utilities, simple Trainer wrapper for sklearn models, PyTorch export+tensor helpers.
- Next Steps: Implement a production Trainer (PyTorch Lightning or native), dataset pipelines, checkpointing, distributed/GPU training examples.

7) RF Fingerprinting — vulture/fingerprinting/*
- Files: `features.py`, `clustering.py`, `classifiers.py`, `anomaly.py`
- Status: Partial
- Purpose: Feature extraction and ML for RF device fingerprinting and anomaly detection.
- Next Steps: Implement richer feature sets (64+), standardized feature vectors, evaluation benchmarks.

8) Spectrum Intelligence — vulture/spectrum/*
- Files: `real_time.py`, `visualization.py`
- Status: Scaffold
- Purpose: Real-time spectrum analyzer interface and visualization primitives for waterfall/spectrum plots.
- Next Steps: Implement real-time processing pipeline, websocket or socket data stream API, GUI integration.

9) Physics Laboratory — vulture/physics/*
- Files: `antenna.py`, `link_budget.py`
- Status: Partial
- Purpose: Antenna effective area, free-space path loss and link budget primitives.
- Next Steps: Add Hata/ITU models, Fresnel calculations, LOS/NLOS heuristics.

10) Dataset Intelligence — vulture/dataset/*
- Files: `io.py`, `validate.py`, `transform.py`
- Status: Partial
- Purpose: Loaders for CSV/JSON/NPY/Parquet with safe fallbacks; schema validation; transforms/cleaning.
- Next Steps: Add SigMF reader, Parquet performance tests, profiling APIs, data validators.

11) Plugin Framework & Model Hub — vulture/plugins + vulture/modelhub (scaffold)
- Status: Scaffold
- Purpose: Plugin discovery, permission model, sandboxed run; model hub for local ONNX models and hashing.
- Next Steps: Implement plugin sandboxes (process/container isolation), permission descriptors and marketplace metadata.

12) CLI & GUI
- CLI: basic parse_args and skeleton implemented in `vulture/cli.py` and `vulture/main.py`.
- GUI: PyQt6 scaffold present — needs wiring to backends and live plotting (pyqtgraph).

---

NEWS.md & change log
- See `NEWS.md` on the feature branch for a batch-by-batch changelog: https://github.com/black-210/VULTURE/blob/feature%2Fadd-scaffold/NEWS.md

Roadmap & priorities (short)
1. PSD & spectrogram (SciPy) + tests
2. RTL-SDR adapter (pyrtlsdr) + mocked tests
3. Peak detection & noise floor estimation
4. PyTorch training loop with checkpointing and example dataset
5. Plugin sandboxing and model hub hardening
6. GUI wiring & live plotting (pyqtgraph)

Contributing
- Work on `feature/*` branches, create PRs to `main`.
- Add tests for new functionality and performance profiles for DSP code.
- Use `black` and `ruff` (pre-commit installed) to maintain code style.

Questions / Next actions — pick one
- I will implement PSD with SciPy now and add tests (`PSD`) — I need permission to push.  
- I will implement an RTL-SDR adapter stub + example (`RTLSDR`) — needs push.  
- Open a Pull Request from `feature/add-scaffold` → `main` with a summary and this README (`PR`).  
- Translate README/NEWS fully to Arabic (`translate`).

---

If you want me to update anything specific in this README (status labels, wording, add more examples or links), say what to change and I will apply it immediately and push the update to the feature branch.
