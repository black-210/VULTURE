"""Capture integrity primitives for receive-only IQ data."""
from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: str | Path, chunk_size: int = 1 << 20) -> str:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iq_byte_count(path: str | Path) -> int:
    size = Path(path).stat().st_size
    if size == 0 or size % 8:
        raise ValueError(".iq capture must contain complete complex64 samples")
    return size
