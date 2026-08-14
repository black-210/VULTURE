"""Framework Registry - Central registration and discovery system."""

from typing import Dict, Any, Type, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class FrameworkMetadata:
    """Metadata for registered framework."""
    name: str
    version: str
    description: str
    author: str
    module_path: str
    entry_point: str
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    enabled: bool = True
    registered_at: datetime = field(default_factory=datetime.now)
    tags: Dict[str, Any] = field(default_factory=dict)


class FrameworkRegistry:
    """Central registry for all VULTURE frameworks."""
    
    def __init__(self):
        self._frameworks: Dict[str, FrameworkMetadata] = {}
        self._instances: Dict[str, Any] = {}
        self._dependencies: Dict[str, List[str]] = {}
        logger.info("FrameworkRegistry initialized")
    
    def register(self, name: str, version: str, description: str, author: str,
                 module_path: str, entry_point: str,
                 dependencies: Optional[List[str]] = None,
                 capabilities: Optional[List[str]] = None,
                 tags: Optional[Dict[str, Any]] = None) -> None:
        """Register a new framework."""
        if name in self._frameworks:
            logger.warning(f"Framework {name} already registered. Overwriting.")
        
        metadata = FrameworkMetadata(
            name=name, version=version, description=description,
            author=author, module_path=module_path, entry_point=entry_point,
            dependencies=dependencies or [],
            capabilities=capabilities or [],
            tags=tags or {}
        )
        
        self._frameworks[name] = metadata
        self._dependencies[name] = dependencies or []
        logger.info(f"Framework '{name}' v{version} registered")
    
    def unregister(self, name: str) -> bool:
        """Unregister a framework."""
        if name in self._frameworks:
            del self._frameworks[name]
            if name in self._instances:
                del self._instances[name]
            del self._dependencies[name]
            logger.info(f"Framework '{name}' unregistered")
            return True
        return False
    
    def get_metadata(self, name: str) -> Optional[FrameworkMetadata]:
        """Get framework metadata."""
        return self._frameworks.get(name)
    
    def get_all_metadata(self) -> Dict[str, FrameworkMetadata]:
        """Get all registered frameworks' metadata."""
        return self._frameworks.copy()
    
    def is_registered(self, name: str) -> bool:
        """Check if framework is registered."""
        return name in self._frameworks
    
    def is_enabled(self, name: str) -> bool:
        """Check if framework is enabled."""
        metadata = self._frameworks.get(name)
        return metadata.enabled if metadata else False
    
    def enable(self, name: str) -> bool:
        """Enable a framework."""
        if name in self._frameworks:
            self._frameworks[name].enabled = True
            logger.info(f"Framework '{name}' enabled")
            return True
        return False
    
    def disable(self, name: str) -> bool:
        """Disable a framework."""
        if name in self._frameworks:
            self._frameworks[name].enabled = False
            logger.info(f"Framework '{name}' disabled")
            return True
        return False
    
    def get_by_capability(self, capability: str) -> List[FrameworkMetadata]:
        """Get all frameworks providing a capability."""
        return [
            metadata for metadata in self._frameworks.values()
            if capability in metadata.capabilities and metadata.enabled
        ]
    
    def get_dependencies(self, name: str) -> List[str]:
        """Get framework dependencies."""
        return self._dependencies.get(name, [])
    
    def validate_dependencies(self, name: str) -> bool:
        """Validate that all dependencies are registered."""
        dependencies = self._dependencies.get(name, [])
        for dep in dependencies:
            if not self.is_registered(dep):
                logger.error(f"Missing dependency: {dep} for {name}")
                return False
        return True
    
    def get_execution_order(self, frameworks: List[str]) -> Optional[List[str]]:
        """Get execution order respecting dependencies."""
        visited = set()
        order = []
        
        def visit(name: str) -> bool:
            if name in visited:
                return True
            if name not in self._frameworks:
                return False
            
            visited.add(name)
            
            for dep in self._dependencies.get(name, []):
                if dep in frameworks and not visit(dep):
                    return False
            
            order.append(name)
            return True
        
        for fw in frameworks:
            if not visit(fw):
                return None
        
        return order
    
    def store_instance(self, name: str, instance: Any) -> None:
        """Store framework instance."""
        self._instances[name] = instance
        logger.debug(f"Instance stored for framework '{name}'")
    
    def get_instance(self, name: str) -> Optional[Any]:
        """Get stored framework instance."""
        return self._instances.get(name)
    
    def clear_instances(self) -> None:
        """Clear all stored instances."""
        self._instances.clear()
        logger.info("All framework instances cleared")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get registry summary."""
        enabled_count = sum(1 for m in self._frameworks.values() if m.enabled)
        return {
            'total_frameworks': len(self._frameworks),
            'enabled_frameworks': enabled_count,
            'disabled_frameworks': len(self._frameworks) - enabled_count,
            'stored_instances': len(self._instances),
            'frameworks': list(self._frameworks.keys()),
        }