"""VULTURE: Production-Grade Intelligence & Research Platform.

Real implementation. Real algorithms. No mockups.
"""

__version__ = "0.1.0"
__author__ = "BLACK Cyber Falcon"
__license__ = "AGPL-3.0"

from vulture.core.framework_registry import FrameworkRegistry
from vulture.core.config_manager import ConfigManager
from vulture.core.dependency_injection import DependencyInjector

__all__ = [
    "FrameworkRegistry",
    "ConfigManager",
    "DependencyInjector",
]
