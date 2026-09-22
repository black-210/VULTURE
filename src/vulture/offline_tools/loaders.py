"""Optional CSV-like numeric fixture loader; no network or device access."""
from __future__ import annotations
from pathlib import Path
from .validation import finite_values


def load_numbers(path: str | Path) -> list[float]:
    text = Path(path).read_text(encoding="utf-8")
    tokens = text.replace(",", " ").split()
    return finite_values([float(token) for token in tokens])
