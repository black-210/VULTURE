"""Configuration Manager - Centralized configuration handling."""

from typing import Dict, Any, Optional, List
from pathlib import Path
import yaml
import json
import logging

logger = logging.getLogger(__name__)


class ConfigurationManager:
    """Manage application configuration from multiple sources."""
    
    def __init__(self):
        self._config: Dict[str, Any] = self._load_defaults()
        self._overrides: Dict[str, Any] = {}
        self._sources: List[str] = []
        logger.info("ConfigurationManager initialized")
    
    @staticmethod
    def _load_defaults() -> Dict[str, Any]:
        """Load default configuration."""
        return {
            'app': {
                'name': 'VULTURE',
                'version': '0.1.0',
                'debug': False,
                'log_level': 'INFO',
            },
            'rf_intelligence': {
                'sample_rate': 1e6,
                'fft_size': 1024,
                'window_type': 'hann',
            },
            'sdr': {
                'sample_rate': 2e6,
                'center_frequency': 2.4e9,
                'gain': 40,
                'device': 'rtlsdr',
            },
            'ml': {
                'framework': 'pytorch',
                'device': 'cpu',
                'batch_size': 32,
                'epochs': 100,
                'learning_rate': 0.001,
            },
            'plugins': {
                'enabled': True,
                'auto_load': True,
                'plugin_dir': './plugins',
                'sandbox': True,
            },
            'security': {
                'verify_signatures': True,
                'audit_logging': True,
                'permission_model': 'rbac',
            },
            'ui': {
                'theme': 'dark',
                'language': 'en',
                'font_size': 10,
            },
            'paths': {
                'data_dir': './data',
                'model_dir': './models',
                'cache_dir': './cache',
                'log_dir': './logs',
            },
        }
    
    def load_yaml(self, path: str) -> bool:
        """Load configuration from YAML file."""
        try:
            with open(path, 'r') as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    self._merge_config(yaml_config)
                    self._sources.append(f"yaml:{path}")
                    logger.info(f"Configuration loaded from {path}")
                    return True
        except Exception as e:
            logger.error(f"Failed to load YAML config from {path}: {e}")
            return False
        return False
    
    def load_json(self, path: str) -> bool:
        """Load configuration from JSON file."""
        try:
            with open(path, 'r') as f:
                json_config = json.load(f)
                if json_config:
                    self._merge_config(json_config)
                    self._sources.append(f"json:{path}")
                    logger.info(f"Configuration loaded from {path}")
                    return True
        except Exception as e:
            logger.error(f"Failed to load JSON config from {path}: {e}")
            return False
        return False
    
    def load_env(self, prefix: str = "VULTURE_") -> None:
        """Load configuration from environment variables."""
        import os
        env_config = {}
        
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                env_config[config_key] = self._parse_env_value(value)
        
        if env_config:
            self._merge_config(env_config)
            self._sources.append(f"env:{prefix}")
            logger.info(f"Configuration loaded from environment (prefix: {prefix})")
    
    @staticmethod
    def _parse_env_value(value: str) -> Any:
        """Parse environment variable value to appropriate type."""
        if value.lower() in ('true', 'yes', '1'):
            return True
        if value.lower() in ('false', 'no', '0'):
            return False
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            return value
    
    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """Deep merge new configuration into current config."""
        def merge_dict(base: Dict, update: Dict) -> Dict:
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
            return base
        
        merge_dict(self._config, new_config)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation."""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        logger.debug(f"Configuration set: {key} = {value}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section."""
        return self._config.get(section, {}).copy()
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration."""
        return self._config.copy()
    
    def has(self, key: str) -> bool:
        """Check if configuration key exists."""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return False
        
        return True
    
    def save_yaml(self, path: str) -> bool:
        """Save configuration to YAML file."""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                yaml.dump(self._config, f, default_flow_style=False)
            logger.info(f"Configuration saved to {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config to {path}: {e}")
            return False
    
    def save_json(self, path: str) -> bool:
        """Save configuration to JSON file."""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                json.dump(self._config, f, indent=2)
            logger.info(f"Configuration saved to {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config to {path}: {e}")
            return False
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self._config = self._load_defaults()
        self._overrides.clear()
        logger.info("Configuration reset to defaults")
    
    def get_sources(self) -> List[str]:
        """Get list of configuration sources loaded."""
        return self._sources.copy()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get configuration summary."""
        def count_keys(d: Dict) -> int:
            count = 0
            for v in d.values():
                if isinstance(v, dict):
                    count += count_keys(v)
                else:
                    count += 1
            return count
        
        return {
            'total_keys': count_keys(self._config),
            'sources_loaded': len(self._sources),
            'sources': self._sources,
        }