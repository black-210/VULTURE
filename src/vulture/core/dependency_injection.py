"""Lightweight DI container with circular dependency detection and lifecycle management."""

import threading
from typing import Any, Callable, Dict, Set, Optional, TypeVar
from enum import Enum
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class Lifecycle(Enum):
    """Dependency lifecycle management."""
    SINGLETON = "singleton"  # One instance per container
    TRANSIENT = "transient"  # New instance each time
    SCOPED = "scoped"  # One instance per scope


class DependencyInjector:
    """Fast, thread-safe DI container with circular dependency detection."""

    def __init__(self):
        self._services: Dict[str, tuple[Callable, Lifecycle]] = {}
        self._singletons: Dict[str, Any] = {}
        self._scopes: Dict[int, Dict[str, Any]] = {}  # scope_id -> instances
        self._current_scope: int = 0
        self._scope_lock = threading.RLock()
        self._lock = threading.RLock()

    def register(self, name: str, factory: Callable, lifecycle: Lifecycle = Lifecycle.SINGLETON) -> None:
        """Register dependency.
        
        Args:
            name: Service name
            factory: Factory callable
            lifecycle: Lifecycle mode
        """
        with self._lock:
            self._services[name] = (factory, lifecycle)
            logger.debug(f"Registered {name} ({lifecycle.value})")

    def resolve(self, name: str, scope_id: Optional[int] = None) -> Any:
        """Resolve dependency.
        
        Args:
            name: Service name
            scope_id: Scope ID for scoped dependencies
            
        Returns:
            Service instance
        """
        return self._resolve(name, set(), scope_id)

    def _resolve(self, name: str, visited: Set[str], scope_id: Optional[int] = None) -> Any:
        """Internal resolve with circular dependency detection."""
        if name in visited:
            raise RuntimeError(f"Circular dependency detected: {' -> '.join(list(visited) + [name])}")
        
        if name not in self._services:
            raise ValueError(f"Service '{name}' not registered")
        
        factory, lifecycle = self._services[name]
        
        # Singleton
        if lifecycle == Lifecycle.SINGLETON:
            with self._lock:
                if name in self._singletons:
                    return self._singletons[name]
                instance = factory()
                self._singletons[name] = instance
                return instance
        
        # Scoped
        elif lifecycle == Lifecycle.SCOPED:
            if scope_id is None:
                scope_id = self._current_scope
            with self._scope_lock:
                if scope_id not in self._scopes:
                    self._scopes[scope_id] = {}
                if name in self._scopes[scope_id]:
                    return self._scopes[scope_id][name]
                instance = factory()
                self._scopes[scope_id][name] = instance
                return instance
        
        # Transient
        else:
            visited.add(name)
            return factory()

    def create_scope(self) -> int:
        """Create new scope.
        
        Returns:
            Scope ID
        """
        with self._scope_lock:
            self._current_scope += 1
            self._scopes[self._current_scope] = {}
            return self._current_scope

    def dispose_scope(self, scope_id: int) -> None:
        """Dispose scope.
        
        Args:
            scope_id: Scope ID
        """
        with self._scope_lock:
            if scope_id in self._scopes:
                # Call dispose() if available on instances
                for instance in self._scopes[scope_id].values():
                    if hasattr(instance, 'dispose'):
                        instance.dispose()
                del self._scopes[scope_id]

    def clear(self) -> None:
        """Clear all services and singletons."""
        with self._lock:
            self._services.clear()
            self._singletons.clear()
            self._scopes.clear()
