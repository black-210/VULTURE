"""Simple Dependency Injection container.

Supports singleton and transient registrations. Lightweight and typed.
"""
from typing import Any, Callable, Dict
from threading import RLock


class Lifetime:
    SINGLETON = "singleton"
    TRANSIENT = "transient"


class DIContainer:
    """A minimal DI container for registering factories and resolving instances."""

    def __init__(self):
        self._factories: Dict[str, Callable] = {}
        self._instances: Dict[str, Any] = {}
        self._lifetimes: Dict[str, str] = {}
        self._lock = RLock()

    def register(self, name: str, factory: Callable[..., Any], lifetime: str = Lifetime.TRANSIENT):
        """Register a factory under a name.

        Args:
            name: registration key
            factory: callable that returns an instance
            lifetime: Lifetime.SINGLETON or Lifetime.TRANSIENT
        """
        with self._lock:
            self._factories[name] = factory
            self._lifetimes[name] = lifetime

    def resolve(self, name: str, *args, **kwargs) -> Any:
        """Resolve an instance by name."""
        with self._lock:
            if name not in self._factories:
                raise KeyError(f"Dependency '{name}' not registered")
            if self._lifetimes.get(name) == Lifetime.SINGLETON:
                if name not in self._instances:
                    self._instances[name] = self._factories[name](*args, **kwargs)
                return self._instances[name]
            return self._factories[name](*args, **kwargs)

    def clear_singletons(self):
        """Clear stored singleton instances."""
        with self._lock:
            self._instances.clear()
