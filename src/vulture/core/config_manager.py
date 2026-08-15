"""Multi-source configuration management: YAML, JSON, Environment."""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional
import logging

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

logger = logging.getLogger(__name__)


class ConfigManager:
    """Unified config from YAML, JSON, environment variables."""

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self._loaded_files: list = []

    def load_yaml(self, path: str) -> None:
        """Load YAML config file.
        
        Args:
            path: Path to YAML file
        """
        if not HAS_YAML:
            raise ImportError("PyYAML required. Install: pip install pyyaml")
        
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(p, 'r') as f:
            data = yaml.safe_load(f)
            self.config.update(data or {})
            self._loaded_files.append(str(p.absolute()))
            logger.info(f"✓ Loaded YAML config: {p}")

    def load_json(self, path: str) -> None:
        """Load JSON config file.
        
        Args:
            path: Path to JSON file
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(p, 'r') as f:
            data = json.load(f)
            self.config.update(data)
            self._loaded_files.append(str(p.absolute()))
            logger.info(f"✓ Loaded JSON config: {p}")

    def load_env(self, prefix: str = "VULTURE_") -> None:
        """Load from environment variables with prefix.
        
        Args:
            prefix: Environment variable prefix
        """
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                # Try to parse as JSON, else use as string
                try:
                    self.config[config_key] = json.loads(value)
                except (json.JSONDecodeError, ValueError):
                    self.config[config_key] = value
        logger.info(f"✓ Loaded environment variables (prefix: {prefix})")

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value with dot notation.
        
        Args:
            key: Config key (supports dot notation: "rf.fft.size")
            default: Default value
            
        Returns:
            Config value
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Set config value with dot notation.
        
        Args:
            key: Config key
            value: Config value
        """
        keys = key.split('.')
        current = self.config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

    def to_dict(self) -> Dict[str, Any]:
        """Get all config as dict.
        
        Returns:
            Config dictionary
        """
        return dict(self.config)

    def save_json(self, path: str) -> None:
        """Save config to JSON file.
        
        Args:
            path: Output path
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, 'w') as f:
            json.dump(self.config, f, indent=2)
        logger.info(f"✓ Saved config to: {p}")
