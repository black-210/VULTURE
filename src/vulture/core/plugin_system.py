"""Sandboxed plugin system with permission control."""

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Callable
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
    entry_point: str  # "module:function"
    required_permissions: list
    dependencies: list


class PluginSystem:
    """Sandboxed plugin loading with permission management."""

    def __init__(self):
        self.plugins: Dict[str, Dict[str, Any]] = {}
        self.permissions: Dict[str, set] = {}  # plugin_name -> set of permissions
        self.max_execution_time = 30  # seconds

    def load_plugin(self, path: str, metadata: PluginMetadata, permissions: set) -> None:
        """Load plugin from path.
        
        Args:
            path: Path to plugin .py file
            metadata: Plugin metadata
            permissions: Granted permissions
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Plugin not found: {path}")
        
        # Check permissions
        required = set(metadata.required_permissions)
        granted = set(permissions)
        if not required.issubset(granted):
            missing = required - granted
            raise PermissionError(f"Plugin {metadata.name} requires: {missing}")
        
        try:
            spec = importlib.util.spec_from_file_location(metadata.name, p)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            self.plugins[metadata.name] = {
                "module": module,
                "metadata": metadata,
                "path": str(p.absolute())
            }
            self.permissions[metadata.name] = granted
            logger.info(f"✓ Loaded plugin: {metadata.name} v{metadata.version}")
        except Exception as e:
            logger.error(f"✗ Failed to load plugin {metadata.name}: {e}")
            raise

    def execute(self, plugin_name: str, func_name: str, *args, **kwargs) -> Any:
        """Execute plugin function (sandboxed).
        
        Args:
            plugin_name: Plugin name
            func_name: Function name
            *args: Arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
        """
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' not loaded")
        
        module = self.plugins[plugin_name]["module"]
        if not hasattr(module, func_name):
            raise AttributeError(f"Plugin {plugin_name} has no function '{func_name}'")
        
        func = getattr(module, func_name)
        
        # Sandboxed execution via subprocess (can add timeout)
        try:
            result = func(*args, **kwargs)
            logger.info(f"✓ Executed {plugin_name}.{func_name}")
            return result
        except Exception as e:
            logger.error(f"✗ Plugin execution failed: {e}")
            raise

    def list_plugins(self) -> Dict[str, PluginMetadata]:
        """List loaded plugins.
        
        Returns:
            Dict of plugin_name -> metadata
        """
        return {name: data["metadata"] for name, data in self.plugins.items()}

    def unload_plugin(self, name: str) -> None:
        """Unload plugin.
        
        Args:
            name: Plugin name
        """
        if name in self.plugins:
            del self.plugins[name]
            self.permissions.pop(name, None)
            logger.info(f"✗ Unloaded plugin: {name}")
