from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_legacy_path = Path(__file__).resolve().parents[1] / "forensics.py"
_spec = importlib.util.spec_from_file_location("vulture._forensics_legacy", _legacy_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"cannot load legacy forensics module: {_legacy_path}")
_legacy = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _legacy
_spec.loader.exec_module(_legacy)

Finding = _legacy.Finding
ForensicReport = _legacy.ForensicReport
audit_chemistry = _legacy.audit_chemistry
audit_mathematics = _legacy.audit_mathematics
audit_physics = _legacy.audit_physics
audit_protocol = _legacy.audit_protocol
write_report = _legacy.write_report

__all__ = ["Finding", "ForensicReport", "audit_chemistry", "audit_mathematics", "audit_physics", "audit_protocol", "write_report"]
