"""Framework Registry - Central component registry and lifecycle management."""

import logging
from typing import Dict, Type, Any, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class FrameworkState(Enum):
    """Framework lifecycle states."""
    UNINITIALIZED = "uninitialized"
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


class BaseFramework(ABC):
    """Abstract base class for all frameworks."""
    
    def __init__(self, name: str, version: str = "0.1.0"):
        """Initialize framework.
        
        Args:
            name: Framework name
            version: Framework version
        """
        self.name = name
        self.version = version
        self.state = FrameworkState.UNINITIALIZED
        self.logger = logging.getLogger(self.name)
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize framework components."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown framework gracefully."""
        pass
    
    def get_state(self) -> FrameworkState:
        """Get current framework state."""
        return self.state


@dataclass
class FrameworkMetadata:
    """Framework metadata."""
    name: str
    version: str
    author: str
    description: str
    dependencies: list = None
    tags: list = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []


class FrameworkRegistry:
    """Central registry for all frameworks."""
    
    def __init__(self):
        """Initialize registry."""
        self._frameworks: Dict[str, BaseFramework] = {}
        self._metadata: Dict[str, FrameworkMetadata] = {}
        self._callbacks: Dict[str, list] = {}
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def register(
        self,
        framework: BaseFramework,
        metadata: FrameworkMetadata,
        auto_init: bool = False
    ) -> None:
        """Register a framework.
        
        Args:
            framework: Framework instance
            metadata: Framework metadata
            auto_init: Auto-initialize on registration
        """
        if framework.name in self._frameworks:
            raise ValueError(f"Framework '{framework.name}' already registered")
        
        # Check dependencies
        for dep in metadata.dependencies:
            if dep not in self._frameworks:
                self.logger.warning(f"Dependency '{dep}' not found for '{framework.name}'")
        
        self._frameworks[framework.name] = framework
        self._metadata[framework.name] = metadata
        
        self.logger.info(f"Registered framework: {framework.name} v{framework.version}")
        
        if auto_init:
            self.initialize(framework.name)
    
    def initialize(self, name: str) -> None:
        """Initialize a framework.
        
        Args:
            name: Framework name
        """
        if name not in self._frameworks:
            raise ValueError(f"Framework '{name}' not found")
        
        framework = self._frameworks[name]
        try:
            framework.initialize()
            framework.state = FrameworkState.INITIALIZED
            self.logger.info(f"Initialized: {name}")
            self._fire_event("framework_initialized", name)
        except Exception as e:
            framework.state = FrameworkState.ERROR
            self.logger.error(f"Failed to initialize {name}: {e}")
            raise
    
    def get(self, name: str) -> Optional[BaseFramework]:
        """Get a framework by name.
        
        Args:
            name: Framework name
        
        Returns:
            Framework instance or None
        """
        return self._frameworks.get(name)
    
    def list_frameworks(self) -> Dict[str, FrameworkMetadata]:
        """List all registered frameworks.
        
        Returns:
            Dictionary of framework metadata
        """
        return self._metadata.copy()
    
    def on(self, event: str, callback: Callable) -> None:
        """Register event callback.
        
        Args:
            event: Event name
            callback: Callback function
        """
        if event not in self._callbacks:
            self._callbacks[event] = []
        self._callbacks[event].append(callback)
    
    def _fire_event(self, event: str, *args, **kwargs) -> None:
        """Fire an event.
        
        Args:
            event: Event name
            args: Event arguments
            kwargs: Event keyword arguments
        """
        if event in self._callbacks:
            for callback in self._callbacks[event]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"Error in callback for {event}: {e}")
    
    def shutdown_all(self) -> None:
        """Shutdown all frameworks gracefully."""
        for name, framework in list(self._frameworks.items()):
            try:
                framework.shutdown()
                framework.state = FrameworkState.STOPPED
                self.logger.info(f"Shutdown: {name}")
            except Exception as e:
                self.logger.error(f"Error shutting down {name}: {e}")
