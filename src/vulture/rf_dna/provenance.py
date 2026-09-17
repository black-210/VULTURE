"""Tamper-evident capture provenance records for RF-DNA review."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json


@dataclass(frozen=True)
class CaptureProvenance:
    capture_id: str
    tenant_id: str
    created_at: str
    source: str
    sample_rate: float
    center_frequency: float
    sample_count: int
    content_sha256: str
    authorization: str

    @classmethod
    def create(cls, *, tenant_id: str, source: str, sample_rate: float,
               center_frequency: float, sample_count: int,
               content_sha256: str, authorization: str) -> "CaptureProvenance":
        payload = f"{tenant_id}|{source}|{sample_rate}|{center_frequency}|{sample_count}|{content_sha256}"
        capture_id = hashlib.sha256(payload.encode()).hexdigest()[:24]
        return cls(capture_id, tenant_id, datetime.now(timezone.utc).isoformat(), source,
                   sample_rate, center_frequency, sample_count, content_sha256, authorization)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def canonical_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))

    def digest(self) -> str:
        return hashlib.sha256(self.canonical_json().encode()).hexdigest()


def verify_provenance(record: dict[str, object]) -> bool:
    """Validate the deterministic capture identifier without trusting UI input."""
    required = {"capture_id", "tenant_id", "source", "sample_rate", "center_frequency",
                "sample_count", "content_sha256", "authorization", "created_at"}
    if not required.issubset(record):
        return False
    copy = dict(record)
    supplied = str(copy.pop("capture_id"))
    payload = f"{copy['tenant_id']}|{copy['source']}|{copy['sample_rate']}|{copy['center_frequency']}|{copy['sample_count']}|{copy['content_sha256']}"
    return supplied == hashlib.sha256(payload.encode()).hexdigest()[:24]
