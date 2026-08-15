# V1.0.0 candidate — Batch B additions

This update adds Batch B prototype features toward v1.0.0:

- GPU acceleration helpers for FFT/PSD (CuPy fallback) — vulture/dsp/fft_gpu.py
- Model Hub (local repository, add/list/verify) — vulture/modelhub/
- ONNX loader utility (onnxruntime optional) — vulture/modelhub/onnx_loader.py
- Model verification helper (SHA256) — vulture/modelhub/verify.py
- Plugin Marketplace MVP and Plugin Sandbox runner (process-based resource limits) — vulture/plugins/
- GUI wiring helper for demo integration — vulture/gui/wire.py

See README.md and ROADMAP for next steps: GPU benchmarks, secure container sandbox, model benchmarking, and GUI live plotting.
