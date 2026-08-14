"""Plugin System - Dynamic extensibility with security."""

import importlib
import sys
from pathlib import Path
from typing import Type, Optional, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class PluginMetadata:
    """Plugin metadata."""
    name: str
    version: str
    author: str
    description: str
    entry_point: str  # Module path to main class
    required_permissions: list = None
    dependencies: list = None
    
    def __post_init__(self):
        if self.required_permissions is None:
            self.required_permissions = []
        if self.dependencies is None:
            self.dependencies = []


class PluginManager:
    """Manage plugin discovery, loading, and execution."""
    
    def __init__(self, plugin_dirs: Optional[list] = None):
        """Initialize plugin manager.
        
        Args:
            plugin_dirs: List of plugin directories to search
        """
        self.plugin_dirs = plugin_dirs or []
        self.loaded_plugins: Dict[str, Any] = {}
        self.metadata: Dict[str, PluginMetadata] = {}
    
    def discover_plugins(self) -> list:
        """Discover available plugins.
        
        Returns:
            List of discovered plugin metadata
        """
        discovered = []
        
        for plugin_dir in self.plugin_dirs:
            path = Path(plugin_dir)
            if not path.exists():
                continue
            
            for entry in path.iterdir():
                if entry.is_dir() and not entry.name.startswith('_'):
                    # Look for plugin_manifest.yaml or __init__.py
                    if (entry / "plugin_manifest.yaml").exists():
                        # Load metadata
                        logger.info(f"Discovered plugin: {entry.name}")
                        discovered.append(entry.name)
        
        return discovered
    
    def load_plugin(self, plugin_name: str, permission_manager: Optional[Any] = None) -> bool:
        """Load a plugin.
        
        Args:
            plugin_name: Plugin name
            permission_manager: Permission manager for authorization
        
        Returns:
            True if loaded successfully
        """
        try:
            if plugin_name in self.loaded_plugins:
                logger.warning(f"Plugin {plugin_name} already loaded")
                return True
            
            # Dynamic import
            module = importlib.import_module(f"plugins.{plugin_name}")
            self.loaded_plugins[plugin_name] = module
            logger.info(f"Loaded plugin: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin.
        
        Args:
            plugin_name: Plugin name
        
        Returns:
            True if unloaded successfully
        """
        if plugin_name in self.loaded_plugins:
            del self.loaded_plugins[plugin_name]
            logger.info(f"Unloaded plugin: {plugin_name}")
            return True
        return False
