# Benchmark instructions

This document explains how to run the PSD/FFT benchmarks included in `vulture/dsp/benchmarks.py`.

Requirements
- Python 3.8+
- numpy, scipy installed
- Optional: cupy installed for GPU benchmarks (install the cupy package matching your CUDA version)

Examples

1) CPU Welch PSD benchmark (random signal):

```bash
python -m vulture.dsp.benchmarks --method welch --samples 1048576 --nperseg 4096 --runs 3
```

2) GPU FFT PSD benchmark (requires CuPy):

```bash
python -m vulture.dsp.benchmarks --method fft_gpu --samples 1048576 --runs 3
```

3) Benchmark using an NPY file as input:

```bash
python -m vulture.dsp.benchmarks --method welch --input path/to/signal.npy --runs 3
```

Interpreting results
- The script prints a JSON summary with per-run timings and mean samples-per-second (throughput).
- Use these numbers to compare CPU vs GPU performance on your hardware.
