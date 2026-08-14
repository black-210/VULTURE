"""Dependency Injection Container - Manage component dependencies."""

from typing import Dict, Any, Type, Callable, Optional, List
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class DependencyInjector:
    """Lightweight dependency injection container."""
    
    def __init__(self):
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._resolving: set = set()
        logger.info("DependencyInjector initialized")
    
    def register_singleton(self, name: str, instance: Any) -> None:
        """Register singleton instance."""
        self._singletons[name] = instance
        logger.debug(f"Singleton registered: {name}")
    
    def register_factory(self, name: str, factory: Callable) -> None:
        """Register factory function for creating instances."""
        self._factories[name] = factory
        logger.debug(f"Factory registered: {name}")
    
    def register_class(self, name: str, cls: Type, **kwargs) -> None:
        """Register class with constructor arguments."""
        def factory():
            return cls(**kwargs)
        self._factories[name] = factory
        logger.debug(f"Class factory registered: {name}")
    
    def get(self, name: str) -> Any:
        """Get service instance (singleton or factory)."""
        if name in self._resolving:
            raise ValueError(f"Circular dependency detected: {name}")
        
        if name in self._singletons:
            return self._singletons[name]
        
        if name not in self._factories:
            raise ValueError(f"Service not registered: {name}")
        
        self._resolving.add(name)
        try:
            instance = self._factories[name]()
            return instance
        finally:
            self._resolving.discard(name)
    
    def get_singleton(self, name: str) -> Optional[Any]:
        """Get singleton if exists, None otherwise."""
        return self._singletons.get(name)
    
    def has(self, name: str) -> bool:
        """Check if service is registered."""
        return name in self._singletons or name in self._factories
    
    def remove(self, name: str) -> bool:
        """Remove service registration."""
        removed = False
        if name in self._singletons:
            del self._singletons[name]
            removed = True
        if name in self._factories:
            del self._factories[name]
            removed = True
        
        if removed:
            logger.debug(f"Service removed: {name}")
        
        return removed
    
    def clear(self) -> None:
        """Clear all registrations."""
        self._singletons.clear()
        self._factories.clear()
        logger.info("DependencyInjector cleared")
    
    def get_registered_services(self) -> List[str]:
        """Get list of all registered services."""
        return list(set(self._singletons.keys()) | set(self._factories.keys()))
    
    def inject(self, **dependencies):
        """Decorator for dependency injection."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                injected = {}
                for dep_name, param_name in dependencies.items():
                    if self.has(dep_name):
                        injected[param_name] = self.get(dep_name)
                
                kwargs.update(injected)
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def get_summary(self) -> Dict[str, Any]:
        """Get injector summary."""
        return {
            'total_singletons': len(self._singletons),
            'total_factories': len(self._factories),
            'total_services': len(self.get_registered_services()),
            'services': self.get_registered_services(),
        }