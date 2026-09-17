"""Small, explainable RF-DNA feature extractor for local IQ data."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import numpy as np


@dataclass(frozen=True)
class Fingerprint:
    digest: str
    sample_count: int
    mean_amplitude: float
    rms_amplitude: float
    peak_amplitude: float
    crest_factor: float
    spectral_centroid_hz: float
    spectral_spread_hz: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def extract_fingerprint(iq: np.ndarray, sample_rate: float) -> Fingerprint:
    """Extract stable descriptive features; this is not a device identity proof."""
    x = np.asarray(iq, dtype=np.complex64).reshape(-1)
    if x.size == 0 or sample_rate <= 0 or not np.isfinite(x).all():
        raise ValueError("IQ must be non-empty and finite; sample_rate must be positive")
    amp = np.abs(x).astype(np.float64)
    power = amp * amp
    spectrum = np.abs(np.fft.rfft(x)) ** 2
    frequencies = np.fft.rfftfreq(x.size, 1.0 / sample_rate)
    total = float(spectrum.sum())
    centroid = float((frequencies * spectrum).sum() / total) if total else 0.0
    spread = float(np.sqrt(((frequencies - centroid) ** 2 * spectrum).sum() / total)) if total else 0.0
    rms = float(np.sqrt(power.mean()))
    return Fingerprint(
        digest=hashlib.sha256(np.ascontiguousarray(x).view(np.uint8)).hexdigest(),
        sample_count=int(x.size),
        mean_amplitude=float(amp.mean()),
        rms_amplitude=rms,
        peak_amplitude=float(amp.max()),
        crest_factor=float(amp.max() / rms) if rms else 0.0,
        spectral_centroid_hz=centroid,
        spectral_spread_hz=spread,
    )


def similarity(left: Fingerprint, right: Fingerprint) -> float:
    """Return a bounded descriptive similarity score in [0, 1]."""
    a = np.array([left.mean_amplitude, left.rms_amplitude, left.crest_factor, left.spectral_centroid_hz, left.spectral_spread_hz], dtype=float)
    b = np.array([right.mean_amplitude, right.rms_amplitude, right.crest_factor, right.spectral_centroid_hz, right.spectral_spread_hz], dtype=float)
    scale = np.maximum(np.maximum(np.abs(a), np.abs(b)), 1e-12)
    distance = float(np.mean(np.abs(a - b) / scale))
    return float(max(0.0, min(1.0, 1.0 - distance)))


def fingerprint_json(fp: Fingerprint) -> str:
    return json.dumps(fp.to_dict(), indent=2, sort_keys=True)
