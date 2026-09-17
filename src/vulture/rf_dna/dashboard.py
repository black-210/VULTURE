"""Safe, offline dashboard and provenance utilities for RF-DNA capture review."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from .fingerprint import extract_fingerprint
from .provenance import CaptureProvenance
from .simulator import generate_iq

try:  # pragma: no cover - optional GUI dependency
    from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QTabWidget, QWidget
    PYQT_AVAILABLE = True
except Exception:  # pragma: no cover
    QApplication = None  # type: ignore[misc,assignment]
    QLabel = None  # type: ignore[misc,assignment]
    QMainWindow = None  # type: ignore[misc,assignment]
    QTabWidget = None  # type: ignore[misc,assignment]
    QWidget = None  # type: ignore[misc,assignment]
    PYQT_AVAILABLE = False


@dataclass
class DashboardCapture:
    label: str
    source: str
    sample_rate: float
    center_frequency: float
    sample_count: int
    digest: str
    fingerprint: dict[str, Any]
    provenance: dict[str, Any]
    tenant_id: str = "local"
    similarity: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = "ready"
        return payload


class RFDNAProvenanceViewer:
    """Review capture records and summarize them for local dashboards."""

    def __init__(self, captures: list[DashboardCapture] | None = None):
        self._captures: list[DashboardCapture] = list(captures or [])

    def add_capture(self, capture: DashboardCapture) -> None:
        self._captures.append(capture)

    def summary(self) -> dict[str, Any]:
        if not self._captures:
            return {"capture_count": 0, "status": "idle", "tenant_ids": [], "latest_digest": None}
        tenant_ids = sorted({capture.tenant_id for capture in self._captures})
        latest = max(self._captures, key=lambda item: item.sample_count)
        return {
            "capture_count": len(self._captures),
            "status": "ready",
            "tenant_ids": tenant_ids,
            "latest_digest": latest.digest,
            "latest_label": latest.label,
            "max_sample_count": latest.sample_count,
            "capture_ids": [capture.digest for capture in self._captures],
        }

    def as_dict(self) -> dict[str, Any]:
        return {"captures": [capture.to_dict() for capture in self._captures], "summary": self.summary()}


def build_dashboard_summary(captures: list[DashboardCapture]) -> dict[str, Any]:
    viewer = RFDNAProvenanceViewer(captures)
    payload = viewer.as_dict()
    payload["tool"] = "rf-dna-dashboard"
    payload["receive_only"] = True
    payload["tls_required_for_remote"] = True
    return payload


def build_capture_from_npz(path: str | Path, label: str = "capture", tenant_id: str = "local") -> DashboardCapture:
    """Construct a dashboard-ready view from a local NPZ capture."""
    with np.load(path) as data:
        if "iq" not in data:
            raise ValueError("NPZ must contain an 'iq' array")
        iq = np.asarray(data["iq"], dtype=np.complex64)
        sample_rate = float(data["sample_rate"]) if "sample_rate" in data else 1.0
    if iq.size == 0:
        raise ValueError("capture must contain samples")
    fingerprint = extract_fingerprint(iq, sample_rate).to_dict()
    provenance = CaptureProvenance.create(
        tenant_id=tenant_id,
        source=str(path),
        sample_rate=sample_rate,
        center_frequency=float(data.get("center_frequency", 0.0)) if hasattr(data, "get") else 0.0,
        sample_count=int(iq.size),
        content_sha256=fingerprint["digest"],
        authorization="operator-approved",
    ).to_dict()
    return DashboardCapture(
        label=label,
        source=str(path),
        sample_rate=sample_rate,
        center_frequency=float(provenance["center_frequency"]),
        sample_count=int(iq.size),
        digest=provenance["capture_id"],
        fingerprint=fingerprint,
        provenance=provenance,
        tenant_id=tenant_id,
        similarity=1.0,
    )


def launch_gui_dashboard(captures: list[DashboardCapture] | None = None) -> bool:
    """Create a lightweight, offline GUI dashboard when PyQt6 is installed."""
    if not PYQT_AVAILABLE:
        return False

    app = QApplication([])
    window = QMainWindow()
    window.setWindowTitle("VULTURE RF-DNA Dashboard")
    tabs = QTabWidget()

    overview = QWidget()
    overview_layout = __import__("PyQt6.QtWidgets").QtWidgets.QVBoxLayout()  # type: ignore[attr-defined]
    overview_layout.addWidget(QLabel("Overview"))
    overview_layout.addWidget(QLabel(f"Capture count: {len(captures or [])}"))
    overview.setLayout(overview_layout)
    tabs.addTab(overview, "Overview")

    provenance = QWidget()
    provenance_layout = __import__("PyQt6.QtWidgets").QtWidgets.QVBoxLayout()  # type: ignore[attr-defined]
    provenance_layout.addWidget(QLabel("Capture provenance viewer"))
    provenance.setLayout(provenance_layout)
    tabs.addTab(provenance, "Provenance")

    window.setCentralWidget(tabs)
    window.resize(900, 600)
    window.show()
    app.exec()
    return True
