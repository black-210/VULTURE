"""Explicit receive-only SDR stream lifecycle helpers."""
from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator
from typing import Any


@contextmanager
def receive_stream(source: Any) -> Iterator[tuple[Any, Any]]:
    """Activate a configured source and always release its stream."""
    device, stream = source.open_soapysdr()
    try:
        yield device, stream
    finally:
        device.deactivateStream(stream)
        device.closeStream(stream)
