#!/usr/bin/env python3
"""
Example script: compute PSD and detect peaks from a saved NPY IQ magnitude file.
"""
import argparse
import numpy as np
from vulture.dsp.psd_scipy import compute_psd
from vulture.dsp.peak_detection import detect_peaks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Path to NPY file containing 1D real signal (magnitude)')
    parser.add_argument('--fs', type=float, default=1.0, help='Sampling rate in Hz')
    args = parser.parse_args()
    data = np.load(args.input)
    out = compute_psd(data, fs=args.fs, method='welch', nperseg=1024)
    peaks = detect_peaks(out['psd'], prominence=0.1)
    print('Found peaks at indices:', peaks['peaks'])

if __name__ == '__main__':
    main()
