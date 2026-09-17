"""Tenant-scoped, authenticated RF-DNA service primitives.

The service is deliberately receive/analyse-only: it accepts bounded IQ feature
jobs, never exposes device discovery or transmission, and requires mTLS when
started with TLS material. Bearer tokens are additionally mapped to tenants.
"""
from __future__ import annotations

import hashlib
import json
import ssl
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
from typing import Any

import numpy as np

from .fingerprint import extract_fingerprint
from .provenance import CaptureProvenance


@dataclass(frozen=True)
class TenantCredential:
    token: str
    tenant_id: str


class TenantStore:
    """Small in-memory store suitable for a single lab service process."""

    def __init__(self, credentials: list[TenantCredential]):
        self._tokens = {item.token: item.tenant_id for item in credentials}
        self._records: dict[str, list[dict[str, Any]]] = {}
        self._lock = Lock()

    def tenant_for(self, token: str) -> str | None:
        return self._tokens.get(token)

    def add_record(self, tenant_id: str, record: dict[str, Any]) -> None:
        with self._lock:
            self._records.setdefault(tenant_id, []).append(record)

    def records_for(self, tenant_id: str) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._records.get(tenant_id, []))


class _RFHandler(BaseHTTPRequestHandler):
    server_version = "VULTURE-RF-DNA/1.0"

    def _reply(self, status: int, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _tenant(self) -> str | None:
        header = self.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return None
        return self.server.store.tenant_for(header[7:].strip())  # type: ignore[attr-defined]

    def do_GET(self) -> None:  # noqa: N802
        tenant = self._tenant()
        if tenant is None:
            self._reply(401, {"error": "authentication required"})
            return
        if self.path != "/v1/captures":
            self._reply(404, {"error": "not found"})
            return
        self._reply(200, {"tenant_id": tenant, "captures": self.server.store.records_for(tenant)})  # type: ignore[attr-defined]

    def do_POST(self) -> None:  # noqa: N802
        tenant = self._tenant()
        if tenant is None:
            self._reply(401, {"error": "authentication required"})
            return
        if self.path != "/v1/fingerprint":
            self._reply(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > self.server.max_body_bytes:  # type: ignore[attr-defined]
                raise ValueError("request body exceeds configured limit")
            body = json.loads(self.rfile.read(length))
            iq = np.asarray(body["iq"], dtype=np.complex64)
            sample_rate = float(body["sample_rate"])
            if iq.size > self.server.max_samples:  # type: ignore[attr-defined]
                raise ValueError("sample limit exceeded")
            fp = extract_fingerprint(iq, sample_rate)
            provenance = CaptureProvenance.create(
                tenant_id=tenant,
                source=str(body.get("source", "service-input")),
                sample_rate=sample_rate,
                center_frequency=float(body.get("center_frequency", 0.0)),
                sample_count=int(iq.size),
                content_sha256=hashlib.sha256(np.ascontiguousarray(iq).view(np.uint8)).hexdigest(),
                authorization=str(body.get("authorization", "operator-approved")),
            )
            record = {"fingerprint": fp.to_dict(), "provenance": provenance.to_dict()}
            self.server.store.add_record(tenant, record)  # type: ignore[attr-defined]
            self._reply(201, record)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            self._reply(400, {"error": str(exc)})

    def log_message(self, *_args: Any) -> None:
        return


class RFDNAService:
    """Threaded HTTPS service; TLS is mandatory, with optional client cert auth."""

    def __init__(self, host: str, port: int, store: TenantStore, *, max_samples: int = 1_000_000):
        self.httpd = ThreadingHTTPServer((host, port), _RFHandler)
        self.httpd.store = store  # type: ignore[attr-defined]
        self.httpd.max_samples = max_samples  # type: ignore[attr-defined]
        self.httpd.max_body_bytes = max(16_000, max_samples * 32)  # type: ignore[attr-defined]

    def configure_tls(self, certfile: str, keyfile: str, ca_file: str) -> None:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile, keyfile)
        context.load_verify_locations(cafile=ca_file)
        context.verify_mode = ssl.CERT_REQUIRED
        self.httpd.socket = context.wrap_socket(self.httpd.socket, server_side=True)

    def serve_forever(self) -> None:
        self.httpd.serve_forever()

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
