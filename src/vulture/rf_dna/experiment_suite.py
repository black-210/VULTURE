"""Benchmarking utilities for quantum-inspired RF experiments with classical baselines."""
from __future__ import annotations

import numpy as np

from .fingerprint import extract_fingerprint


def run_quantum_experiment(iq: np.ndarray, sample_rate: float, *, seed: int = 7) -> dict[str, object]:
    """Return a compact quantum-classical comparison for offline analysis.

    This intentionally remains SDK-free; it compares a QFT-like proxy against a
    classical FFT baseline and always includes a classical baseline metric.
    """
    x = np.asarray(iq, dtype=np.complex128).reshape(-1)
    if x.size == 0 or sample_rate <= 0:
        raise ValueError("iq must be non-empty and sample_rate must be positive")
    n = min(x.size, 256)
    signal = x[:n]
    classical = np.fft.fft(signal) / np.sqrt(n)
    qft = np.exp(-2j * np.pi * np.outer(np.arange(n), np.arange(n)) / n) @ signal / np.sqrt(n)
    rng = np.random.default_rng(seed)
    probs = np.abs(qft) ** 2
    probs = probs / (probs.sum() or 1.0)
    counts = rng.multinomial(256, probs)
    fp = extract_fingerprint(signal, sample_rate)
    return {
        "experiment": "qft-vs-fft",
        "sample_count": int(signal.size),
        "sample_rate": float(sample_rate),
        "classical_fft_norm": float(np.linalg.norm(classical)),
        "qft_proxy_norm": float(np.linalg.norm(qft)),
        "qft_proxy_error": float(np.linalg.norm(classical - qft)),
        "fingerprint_digest": fp.digest,
        "classical_baseline_score": float(np.mean(np.abs(classical) ** 2)),
        "counts": counts.tolist(),
        "seed": seed,
        "status": "ready",
    }


def classical_baseline_accuracy(features: np.ndarray, labels: np.ndarray) -> dict[str, float]:
    """Nearest-centroid classical baseline for small experiments."""
    x = np.asarray(features, dtype=float)
    y = np.asarray(labels)
    if x.ndim != 2 or x.shape[0] != y.shape[0]:
        raise ValueError("features must be 2D and align with labels")
    classes = np.unique(y)
    centroids = {label: x[y == label].mean(axis=0) for label in classes}
    predictions = np.array([min(classes, key=lambda item: np.linalg.norm(row - centroids[item])) for row in x])
    return {
        "accuracy": float(np.mean(predictions == y)),
        "samples": float(x.shape[0]),
        "classes": float(len(classes)),
    }
