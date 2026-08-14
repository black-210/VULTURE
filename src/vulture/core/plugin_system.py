"""Plugin System - Extensible plugin architecture with security."""

from typing import Dict, Any, Optional, List
from pathlib import Path
import importlib.util
import logging

logger = logging.getLogger(__name__)


class PluginMetadata:
    """Plugin metadata and manifest."""
    
    def __init__(self, name: str, version: str, description: str, author: str,
                 entry_point: str, capabilities: Optional[List[str]] = None,
                 required_permissions: Optional[List[str]] = None,
                 dependencies: Optional[List[str]] = None,
                 checksum: Optional[str] = None):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.entry_point = entry_point
        self.capabilities = capabilities or []
        self.required_permissions = required_permissions or []
        self.dependencies = dependencies or []
        self.checksum = checksum
        self.enabled = False
        self.loaded = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'author': self.author,
            'entry_point': self.entry_point,
            'capabilities': self.capabilities,
            'required_permissions': self.required_permissions,
            'dependencies': self.dependencies,
            'enabled': self.enabled,
            'loaded': self.loaded,
        }


class PluginSystem:
    """Manage plugin discovery, loading, and execution."""
    
    def __init__(self, plugin_dir: str = "./plugins", sandbox: bool = True):
        self._plugin_dir = Path(plugin_dir)
        self._plugins: Dict[str, PluginMetadata] = {}
        self._instances: Dict[str, Any] = {}
        self._sandbox = sandbox
        self._permissions: Dict[str, set] = {}
        logger.info(f"PluginSystem initialized (sandbox: {sandbox})")
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins in plugin directory."""
        if not self._plugin_dir.exists():
            self._plugin_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created plugin directory: {self._plugin_dir}")
            return []
        
        discovered = []
        for path in self._plugin_dir.glob("*/manifest.json"):
            try:
                import json
                with open(path, 'r') as f:
                    manifest = json.load(f)
                
                metadata = PluginMetadata(
                    name=manifest['name'],
                    version=manifest['version'],
                    description=manifest['description'],
                    author=manifest['author'],
                    entry_point=manifest['entry_point'],
                    capabilities=manifest.get('capabilities', []),
                    required_permissions=manifest.get('required_permissions', []),
                    dependencies=manifest.get('dependencies', []),
                )
                
                self._plugins[metadata.name] = metadata
                discovered.append(metadata.name)
                logger.info(f"Plugin discovered: {metadata.name}")
            except Exception as e:
                logger.error(f"Failed to load plugin manifest from {path}: {e}")
        
        return discovered
    
    def register_plugin(self, metadata: PluginMetadata) -> bool:
        """Register plugin metadata."""
        if metadata.name in self._plugins:
            logger.warning(f"Plugin {metadata.name} already registered")
            return False
        
        self._plugins[metadata.name] = metadata
        logger.info(f"Plugin registered: {metadata.name}")
        return True
    
    def load_plugin(self, name: str, permissions: Optional[List[str]] = None) -> bool:
        """Load and initialize plugin."""
        if name not in self._plugins:
            logger.error(f"Plugin not found: {name}")
            return False
        
        metadata = self._plugins[name]
        plugin_path = self._plugin_dir / name / f"{metadata.entry_point}.py"
        
        if not plugin_path.exists():
            logger.error(f"Plugin file not found: {plugin_path}")
            return False
        
        try:
            spec = importlib.util.spec_from_file_location(f"vulture_plugin_{name}", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'Plugin'):
                plugin_class = module.Plugin
                instance = plugin_class()
                self._instances[name] = instance
                metadata.loaded = True
                metadata.enabled = True
                
                if permissions:
                    self._permissions[name] = set(permissions)
                
                logger.info(f"Plugin loaded: {name} v{metadata.version}")
                return True
            else:
                logger.error(f"Plugin {name} missing 'Plugin' class")
                return False
        except Exception as e:
            logger.error(f"Failed to load plugin {name}: {e}")
            return False
    
    def unload_plugin(self, name: str) -> bool:
        """Unload plugin."""
        if name not in self._instances:
            return False
        
        try:
            instance = self._instances[name]
            if hasattr(instance, 'cleanup'):
                instance.cleanup()
            
            del self._instances[name]
            self._plugins[name].loaded = False
            self._plugins[name].enabled = False
            
            if name in self._permissions:
                del self._permissions[name]
            
            logger.info(f"Plugin unloaded: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to unload plugin {name}: {e}")
            return False
    
    def get_plugin_instance(self, name: str) -> Optional[Any]:
        """Get loaded plugin instance."""
        return self._instances.get(name)
    
    def get_plugin_metadata(self, name: str) -> Optional[PluginMetadata]:
        """Get plugin metadata."""
        return self._plugins.get(name)
    
    def get_all_plugins(self) -> Dict[str, PluginMetadata]:
        """Get all registered plugins' metadata."""
        return self._plugins.copy()
    
    def get_loaded_plugins(self) -> List[str]:
        """Get list of loaded plugins."""
        return list(self._instances.keys())
    
    def has_permission(self, plugin_name: str, permission: str) -> bool:
        """Check if plugin has permission."""
        if not self._sandbox:
            return True
        
        perms = self._permissions.get(plugin_name, set())
        return permission in perms
    
    def grant_permission(self, plugin_name: str, permission: str) -> bool:
        """Grant permission to plugin."""
        if plugin_name not in self._plugins:
            return False
        
        if plugin_name not in self._permissions:
            self._permissions[plugin_name] = set()
        
        self._permissions[plugin_name].add(permission)
        logger.info(f"Permission '{permission}' granted to plugin '{plugin_name}'")
        return True
    
    def revoke_permission(self, plugin_name: str, permission: str) -> bool:
        """Revoke permission from plugin."""
        if plugin_name not in self._permissions:
            return False
        
        self._permissions[plugin_name].discard(permission)
        logger.info(f"Permission '{permission}' revoked from plugin '{plugin_name}'")
        return True
    
    def get_summary(self) -> Dict[str, Any]:
        """Get plugin system summary."""
        return {
            'total_plugins': len(self._plugins),
            'loaded_plugins': len(self._instances),
            'sandbox_enabled': self._sandbox,
            'loaded_plugin_names': self.get_loaded_plugins(),
        }