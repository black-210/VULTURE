"""JSON serialization helpers with explicit deterministic formatting."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any


def dump(payload: Any, path: str | Path | None = None) -> str:
    text = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False)
    if path is not None:
        Path(path).write_text(text + "\n", encoding="utf-8")
    return text
