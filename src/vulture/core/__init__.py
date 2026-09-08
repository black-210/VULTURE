"""VULTURE Core Engine - Framework Registry, Dependency Injection, Configuration."""
from .framework_registry import FrameworkRegistry
from .dependency_injection import DependencyInjection
from .dependency_injection import DependencyInjection as DependencyInjector
from .config_manager import ConfigurationManager
from .config import ConfigManager
from .permission_manager import PermissionManager
from .plugin_system import PluginSystem
from .security_policy import SecurityPolicy

__all__ = ['FrameworkRegistry', 'DependencyInjection', 'DependencyInjector',
           'ConfigurationManager', 'ConfigManager', 'PermissionManager',
           'PluginSystem', 'SecurityPolicy']
