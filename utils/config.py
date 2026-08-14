"""Configuration management for TERFALCOM."""
import yaml
from pathlib import Path
from typing import Any, Dict, Optional

class Config:
    """Configuration loader and manager."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to YAML config file. If None, uses defaults.
        """
        self.config = self._load_defaults()
        if config_path:
            self.load_yaml(config_path)
    
    @staticmethod
    def _load_defaults() -> Dict[str, Any]:
        """Load default configuration."""
        return {
            'rf_fingerprinting': {
                'sample_rate': 1e6,  # 1 MHz
                'fft_size': 1024,
                'n_features': 64,
                'clustering_algorithm': 'kmeans',
                'n_clusters': 5,
            },
            'model_hub': {
                'model_dir': './models',
                'enable_verification': True,
            },
            'ai_orchestration': {
                'default_adapter': 'mock',
                'timeout_seconds': 30,
                'max_retries': 3,
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        }
    
    def load_yaml(self, config_path: str) -> None:
        """Load configuration from YAML file.
        
        Args:
            config_path: Path to YAML configuration file.
        """
        with open(config_path, 'r') as f:
            yaml_config = yaml.safe_load(f)
            if yaml_config:
                self.config.update(yaml_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation.
        
        Args:
            key: Configuration key (e.g., 'rf_fingerprinting.fft_size')
            default: Default value if key not found.
        
        Returns:
            Configuration value or default.
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
            key: Configuration key (e.g., 'rf_fingerprinting.fft_size')
            value: Value to set.
        """
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
