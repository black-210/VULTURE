"""Framework registry: thread-safe registry for components and plugins.

Lightweight, production-minded registry with simple lifecycle tracking.
"""

from threading import RLock
from typing import Any, Dict


class FrameworkRegistry:
    """Thread-safe registry for framework components.

    Usage:
        reg = FrameworkRegistry()
        reg.register("fft", FFTAnalyzer)
        cls = reg.get("fft")
    """

    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._lock = RLock()

    def register(self, name: str, value: Any) -> None:
        """Register a component by name. Overwrites existing entry.

        Args:
            name: key name
            value: component (class, function, instance)
        """
        with self._lock:
            self._store[name] = value

    def get(self, name: str, default: Any = None) -> Any:
        """Retrieve a registered component.

        Returns default if not found.
        """
        with self._lock:
            return self._store.get(name, default)

    def list(self):
        """List registered keys."""
        with self._lock:
            return list(self._store.keys())
