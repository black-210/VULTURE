"""Central registry for all frameworks. Fast, thread-safe, discoverable."""

import threading
from typing import Any, Dict, Callable, Optional, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class FrameworkMetadata:
    """Metadata for registered framework."""
    name: str
    version: str
    module_path: str
    description: str
    dependencies: List[str]
    category: str  # "rf", "ml", "dsp", "security", etc
    is_production: bool = True
    author: str = "BLACK Cyber Falcon"


class FrameworkRegistry:
    """Fast, thread-safe framework registry with circular dependency detection."""

    def __init__(self):
        self._frameworks: Dict[str, FrameworkMetadata] = {}
        self._factory: Dict[str, Callable] = {}
        self._instances: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._categories: Dict[str, List[str]] = {}

    def register(self, metadata: FrameworkMetadata, factory: Callable) -> None:
        """Register framework with metadata and factory.
        
        Args:
            metadata: Framework metadata
            factory: Callable that creates instances
        """
        with self._lock:
            if metadata.name in self._frameworks:
                logger.warning(f"Framework '{metadata.name}' already registered. Overwriting.")
            
            self._frameworks[metadata.name] = metadata
            self._factory[metadata.name] = factory
            
            # Index by category
            if metadata.category not in self._categories:
                self._categories[metadata.category] = []
            self._categories[metadata.category].append(metadata.name)
            
            logger.info(f"✓ Registered {metadata.category}/{metadata.name} v{metadata.version}")

    def get(self, name: str, singleton: bool = True) -> Any:
        """Get framework instance (cached or fresh).
        
        Args:
            name: Framework name
            singleton: Cache instance
            
        Returns:
            Framework instance
        """
        with self._lock:
            if name not in self._frameworks:
                raise ValueError(f"Framework '{name}' not registered")
            
            if singleton and name in self._instances:
                return self._instances[name]
            
            # Check dependencies
            self._check_circular_deps(name, set())
            
            instance = self._factory[name]()
            if singleton:
                self._instances[name] = instance
            return instance

    def _check_circular_deps(self, name: str, visited: set) -> None:
        """Detect circular dependencies.
        
        Args:
            name: Framework name
            visited: Already visited frameworks
        """
        if name in visited:
            raise RuntimeError(f"Circular dependency detected involving '{name}'")
        
        visited.add(name)
        deps = self._frameworks[name].dependencies
        for dep in deps:
            if dep in self._frameworks:
                self._check_circular_deps(dep, visited.copy())

    def list_by_category(self, category: str) -> List[FrameworkMetadata]:
        """List all frameworks in category.
        
        Args:
            category: Category name
            
        Returns:
            List of framework metadata
        """
        names = self._categories.get(category, [])
        return [self._frameworks[name] for name in names]

    def get_metadata(self, name: str) -> FrameworkMetadata:
        """Get framework metadata.
        
        Args:
            name: Framework name
            
        Returns:
            Framework metadata
        """
        if name not in self._frameworks:
            raise ValueError(f"Framework '{name}' not registered")
        return self._frameworks[name]

    def list_all(self) -> Dict[str, FrameworkMetadata]:
        """List all registered frameworks.
        
        Returns:
            Dict of framework name -> metadata
        """
        with self._lock:
            return dict(self._frameworks)

    def unregister(self, name: str) -> None:
        """Unregister framework.
        
        Args:
            name: Framework name
        """
        with self._lock:
            if name in self._frameworks:
                metadata = self._frameworks.pop(name)
                self._factory.pop(name, None)
                self._instances.pop(name, None)
                if metadata.category in self._categories:
                    self._categories[metadata.category].remove(name)
                logger.info(f"✗ Unregistered {metadata.category}/{name}")

    def clear(self) -> None:
        """Clear all registrations."""
        with self._lock:
            self._frameworks.clear()
            self._factory.clear()
            self._instances.clear()
            self._categories.clear()
            logger.info("✗ Cleared all framework registrations")
