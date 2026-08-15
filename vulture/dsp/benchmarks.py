"""
PSD & FFT benchmark utilities.
Measure PSD computation throughput (samples/sec) and per-run timing for Welch and FFT-based PSD.
"""
import argparse
import time
import json
import numpy as np
from typing import Tuple

from vulture.dsp.psd_scipy import compute_psd
from vulture.dsp.fft_gpu import compute_psd_gpu


def bench_welch(samples: np.ndarray, fs: float, nperseg: int) -> Tuple[float, int]:
    t0 = time.perf_counter()
    out = compute_psd(samples, fs=fs, method='welch', nperseg=nperseg)
    t1 = time.perf_counter()
    return t1 - t0, len(samples)


def bench_fft_gpu(samples: np.ndarray, fs: float) -> Tuple[float, int]:
    t0 = time.perf_counter()
    freqs, psd = compute_psd_gpu(samples, fs=fs)
    t1 = time.perf_counter()
    return t1 - t0, len(samples)


def run_bench(args):
    # prepare samples
    if args.input is not None:
        sig = np.load(args.input)
    else:
        sig = np.random.randn(args.samples)

    runs = []
    for i in range(args.runs):
        if args.method == 'welch':
            t, n = bench_welch(sig, args.fs, args.nperseg)
        elif args.method == 'fft_gpu':
            t, n = bench_fft_gpu(sig, args.fs)
        else:
            raise SystemExit('Unknown method')
        runs.append({'run': i, 'time_sec': t, 'samples': n, 'samples_per_sec': n / t if t > 0 else None})
        if args.inter_run_sleep:
            time.sleep(args.inter_run_sleep)

    summary = {
        'method': args.method,
        'samples': len(sig),
        'fs': args.fs,
        'nperseg': args.nperseg,
        'runs': runs,
        'mean_sps': sum(r['samples_per_sec'] for r in runs if r['samples_per_sec']) / len(runs)
    }
    print(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', choices=['welch', 'fft_gpu'], default='welch')
    parser.add_argument('--input', help='Path to NPY file with signal samples')
    parser.add_argument('--samples', type=int, default=1048576)
    parser.add_argument('--fs', type=float, default=1.0)
    parser.add_argument('--nperseg', type=int, default=4096)
    parser.add_argument('--runs', type=int, default=3)
    parser.add_argument('--inter-run-sleep', type=float, default=0.5)
    args = parser.parse_args()
    run_bench(args)

if __name__ == '__main__':
    main()
