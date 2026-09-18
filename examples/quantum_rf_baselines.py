"""Deterministic quantum-inspired experiments with mandatory classical baselines.

No quantum SDK is required. The optional SDK hook is intentionally separate so
ordinary RF-DNA installations remain offline and reproducible.
"""
from __future__ import annotations

import numpy as np


def qft_vs_fft(samples: np.ndarray, shots: int = 256, seed: int = 7) -> dict[str, object]:
    """Compare a normalized DFT proxy with NumPy FFT and report an error baseline."""
    x = np.asarray(samples, dtype=np.complex128).reshape(-1)
    if x.size == 0 or x.size > 256:
        raise ValueError("samples must contain 1..256 values")
    classical = np.fft.fft(x) / np.sqrt(x.size)
    quantum_proxy = np.exp(-2j * np.pi * np.outer(np.arange(x.size), np.arange(x.size)) / x.size) @ x / np.sqrt(x.size)
    rng = np.random.default_rng(seed)
    probabilities = np.abs(quantum_proxy) ** 2
    probabilities /= probabilities.sum() or 1.0
    counts = rng.multinomial(shots, probabilities)
    return {"experiment": "qft_vs_fft", "n_qubits": int(np.ceil(np.log2(x.size))),
            "shots": shots, "seed": seed, "classical_fft_norm": float(np.linalg.norm(classical)),
            "proxy_error": float(np.linalg.norm(classical - quantum_proxy)), "counts": counts.tolist()}


def classical_baseline(features: np.ndarray, labels: np.ndarray) -> dict[str, float]:
    """Provide an auditable nearest-centroid baseline for small experiments."""
    x, y = np.asarray(features, dtype=float), np.asarray(labels)
    if x.ndim != 2 or len(x) != len(y) or len(x) < 2:
        raise ValueError("features and labels must describe at least two samples")
    classes = np.unique(y)
    centroids = {c: x[y == c].mean(axis=0) for c in classes}
    prediction = np.array([min(classes, key=lambda c: np.linalg.norm(row - centroids[c])) for row in x])
    return {"accuracy": float(np.mean(prediction == y)), "samples": float(len(y)), "classes": float(len(classes))}
def main():
    """Run the experiments and print the results."""
    samples = np.random.normal(size=256)
    shots = 256
    seed = 7
    results = qft_vs_fft(samples, shots, seed)
    print(results)
    features = np.random.normal(size=(100, 2))
    labels = np.random.randint(0, 2, size=100)
    baseline = classical_baseline(features, labels)
    print(baseline)
