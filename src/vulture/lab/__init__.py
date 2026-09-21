from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_legacy_path = Path(__file__).resolve().parents[1] / "lab.py"
_spec = importlib.util.spec_from_file_location("vulture._lab_legacy", _legacy_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"cannot load legacy lab module: {_legacy_path}")
_legacy = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _legacy
_spec.loader.exec_module(_legacy)

LabResult = _legacy.LabResult
attack_simulation = _legacy.attack_simulation
defense_simulation = _legacy.defense_simulation

__all__ = ["LabResult", "attack_simulation", "defense_simulation"]
