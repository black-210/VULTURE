"""Configuration Management System."""

import yaml
import json
from pathlib import Path
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """Centralized configuration management."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize config manager.
        
        Args:
            config_dir: Configuration directory path
        """
        self.config_dir = Path(config_dir) if config_dir else Path.home() / ".vulture"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config: Dict[str, Any] = self._load_defaults()
    
    @staticmethod
    def _load_defaults() -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "rf_intelligence": {
                "fft_size": 2048,
                "sample_rate": 1e6,
                "window": "hann",
            },
            "ai_intelligence": {
                "default_provider": "local",
                "timeout_seconds": 60,
            },
            "ml_framework": {
                "gpu_enabled": True,
                "batch_size": 32,
                "num_workers": 4,
            },
            "security": {
                "enable_sandboxing": True,
                "enable_audit_log": True,
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        }
    
    def load_yaml(self, path: str) -> None:
        """Load YAML configuration file.
        
        Args:
            path: Path to YAML file
        """
        try:
            with open(path, 'r') as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    self.config.update(yaml_config)
            logger.info(f"Loaded config from {path}")
        except Exception as e:
            logger.error(f"Failed to load config {path}: {e}")
    
    def save_yaml(self, path: str) -> None:
        """Save configuration to YAML file.
        
        Args:
            path: Path to save YAML
        """
        try:
            with open(path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            logger.info(f"Saved config to {path}")
        except Exception as e:
            logger.error(f"Failed to save config {path}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation.
        
        Args:
            key: Config key (e.g., 'rf_intelligence.fft_size')
            default: Default value
        
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by dot notation.
        
        Args:
            key: Config key
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
