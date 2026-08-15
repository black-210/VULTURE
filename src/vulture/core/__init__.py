"""Core engine: Registry, DI, Config, Plugin System, Security."""

from vulture.core.framework_registry import FrameworkRegistry
from vulture.core.dependency_injection import DependencyInjector
from vulture.core.config_manager import ConfigManager
from vulture.core.plugin_system import PluginSystem, PluginMetadata
from vulture.core.security_policy import SecurityPolicy, RBAC

__all__ = [
    "FrameworkRegistry",
    "DependencyInjector",
    "ConfigManager",
    "PluginSystem",
    "PluginMetadata",
    "SecurityPolicy",
    "RBAC",
]
