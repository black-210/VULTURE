# VULTURE 🦅 — Unified RF/SDR/DSP/ML Platform (v1.0.0-candidate)

This README summarizes the current state of the repository, what was added in Batch A and Batch B, how to run and test the code, and the remaining work to reach a production-grade v1.0.0 release. The feature branch `feature/add-scaffold` contains all changes described below.

Status overview
---------------
- Branch: feature/add-scaffold
- Release target: v1.0.0 (candidate)
- Batch A: Delivered — PSD (Welch/Periodogram), Spectrogram, Peak detection, RTL-SDR adapter (pyrtlsdr wrapper), TorchTrainer, unit tests, examples.
- Batch B: Delivered — GPU FFT helpers (CuPy fallback), Model Hub (add/list/verify), ONNX loader helper, Plugin Marketplace MVP, Plugin Sandbox (process-based), GUI wiring helper, basic benchmarks and NEWS update.

Current readiness (short)
-------------------------
- Many frameworks are scaffolded and contain working implementations suitable for prototyping and research. See the per-framework Status matrix in the ROADMAP section of this README.
- The repository is now a v1.0.0 candidate with core MVP functionality implemented. Further production hardening (secure sandboxing, deep performance tuning, integration tests with real hardware, hardened CI with GPU runners) is required before a production release.

What's new in this branch
-------------------------
- DSP: vulture/dsp/psd_scipy.py, vulture/dsp/spectrogram_real.py, vulture/dsp/peak_detection.py, vulture/dsp/fft_gpu.py
- SDR: vulture/sdr/rtl.py — RTL-SDR device wrapper (pyrtlsdr)
- ML: vulture/ml/torch_trainer.py — PyTorch Trainer skeleton (fit, checkpoint, ONNX export)
- Model Hub: vulture/modelhub/{repo.py,onnx_loader.py,verify.py}
- Plugins: vulture/plugins/{marketplace.py,sandbox.py} + vulture/plugins/sandbox_docker.py (Docker-runner shim)
- GUI: vulture/gui/wire.py (wiring helper for demos)
- Benchmarks & examples: examples/psd_example.py, vulture/dsp/benchmarks.py, docs/benchmark.md
- Tests: tests/* covering PSD, peak detection, RTL wrapper (hardware-aware skip), TorchTrainer, ModelHub, Sandbox
- NEWS.md updated with Batch A & B notes
- RELEASE_NOTES/v1.0.0-rc.1.md (draft)

How to run and validate locally
--------------------------------
1) Checkout the feature branch

```bash
git fetch origin
git checkout feature/add-scaffold
```

2) Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate     # Windows PowerShell
pip install --upgrade pip
# Core packages
pip install pytest numpy scipy matplotlib
# Optional (for hardware/testing/ML/GPU)
pip install pyrtlsdr torch onnxruntime
# Optional GPU (CuPy) - install matching your CUDA version if available
# pip install cupy-cuda11x  # choose correct package for your CUDA
```

3) Run unit tests

```bash
pytest -q
```

4) Run PSD example

```bash
python examples/psd_example.py path/to/signal.npy --fs 1e6
```

5) Run PSD benchmark (measures throughput and latency)

```bash
python -m vulture.dsp.benchmarks --method welch --samples 1048576 --nperseg 4096 --runs 3
```

Notes about hardware and optional dependencies
---------------------------------------------
- pyrtlsdr requires the system library librtlsdr (install via apt/brew) and access to a USB RTL-SDR device to run hardware tests. The tests are written to skip automatically if hardware is not available.
- CuPy installation depends on your CUDA version and is optional. If CuPy is not installed, code falls back to NumPy CPU paths.
- ONNX runtime is optional and used only if present for model loading.

Batch B completion and what remains for production
-------------------------------------------------
What we completed in Batch B (now in this branch):
- GPU FFT helper for faster transforms where CuPy is installed.
- Model Hub: local storage and SHA verification for ONNX models.
- Plugin marketplace MVP and a process-based sandbox runner with optional memory limits (Unix).
- A Docker-based sandbox shim (attempts `docker run`, falls back to process sandbox) for environments that prefer container isolation.
- Basic benchmarking utilities to measure PSD throughput.

Remaining high-priority items before declaring v1.0.0 production-ready:
1. Hardened plugin sandbox (container orchestration / seccomp / AppArmor / user namespaces).  
2. Integration tests with multiple SDR hardware (RTL-SDR, UHD/USRP, PlutoSDR) and CI runners that can access mock hardware or dedicated test beds.  
3. GPU performance benchmarks on CI/GPU runners and CI acceleration for test matrix where applicable.  
4. Full PyTorch training pipelines with dataset recipes and end-to-end examples.  
5. GUI wiring and live plotting improvements (pyqtgraph integration and demo apps).  
6. Security audit of plugin execution paths and model loading.  

Release candidate and next steps
--------------------------------
- This branch is a v1.0.0 candidate. I can open a PR to `main` with a release draft and the checklist if you want. After the PR we continue with the production hardening tasks listed above (these are Batch B → production tasks).

If you want me to open the PR now, say "افتح PR" and I will prepare the PR title, description, checklist and steps to merge. If you want me to tag the branch as v1.0.0-rc.1, say "انسخها وعلّم" and I'll prepare the release tag (I can provide the git commands for you to run).

Thanks — the candidate is in the branch and ready for review. If you want me to push further production hardening items immediately, tell me which priority item to start next and I'll implement it and add tests.
