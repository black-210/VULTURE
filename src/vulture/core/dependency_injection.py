"""Dependency Injection Container

Manages service registration and resolution with circular dependency detection.
"""

from typing import Dict, Any, Callable, Optional, Set
import logging


class CircularDependencyError(Exception):
    """Raised when circular dependency is detected"""
    pass


class DependencyInjection:
    """Dependency Injection Container"""
    
    def __init__(self):
        self.services: Dict[str, Any] = {}
        self.factories: Dict[str, Callable] = {}
        self.singletons: Set[str] = set()
        self.logger = logging.getLogger("vulture.di")
        self._resolving: Set[str] = set()
    
    def register(self, name: str, service: Any, singleton: bool = True) -> None:
        """Register a service instance"""
        self.services[name] = service
        if singleton:
            self.singletons.add(name)
        self.logger.debug(f"Registered service: {name}")
    
    def register_factory(self, name: str, factory: Callable, singleton: bool = False) -> None:
        """Register a factory function"""
        self.factories[name] = factory
        if singleton:
            self.singletons.add(name)
        self.logger.debug(f"Registered factory: {name}")
    
    def resolve(self, name: str) -> Any:
        """Resolve a service with circular dependency detection"""
        if name in self._resolving:
            raise CircularDependencyError(f"Circular dependency detected for {name}")
        
        self._resolving.add(name)
        try:
            # Check if already resolved singleton
            if name in self.services and name in self.singletons:
                return self.services[name]
            
            # Try factory
            if name in self.factories:
                service = self.factories[name]()
                if name in self.singletons:
                    self.services[name] = service
                return service
            
            # Try direct service
            if name in self.services:
                return self.services[name]
            
            raise KeyError(f"Service {name} not found")
        finally:
            self._resolving.discard(name)
    
    def has(self, name: str) -> bool:
        """Check if service is registered"""
        return name in self.services or name in self.factories


# Alias for backward compatibility
Container = DependencyInjection
