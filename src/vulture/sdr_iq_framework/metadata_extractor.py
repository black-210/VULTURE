"""JSON metadata management for recordings."""

import json
from pathlib import Path
from typing import Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MetadataManager:
    """Metadata management for IQ recordings."""

    def __init__(self, base_file: str):
        """
        Args:
            base_file: Base filename (metadata saved as base_file.json)
        """
        self.base_file = Path(base_file)
        self.meta_file = self.base_file.with_suffix('.meta.json')
        self.metadata: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Set metadata value.
        
        Args:
            key: Key (supports nested: "rf.center_freq")
            value: Value
        """
        keys = key.split('.')
        current = self.metadata
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get metadata value.
        
        Args:
            key: Key (dot notation)
            default: Default if not found
            
        Returns:
            Value or default
        """
        keys = key.split('.')
        current = self.metadata
        for k in keys:
            if isinstance(current, dict):
                current = current.get(k)
                if current is None:
                    return default
            else:
                return default
        return current if current is not None else default

    def save(self) -> None:
        """Save metadata to JSON file."""
        try:
            with open(self.meta_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            logger.info(f"✓ Metadata saved to {self.meta_file}")
        except Exception as e:
            logger.error(f"✗ Save failed: {e}")

    def load(self) -> None:
        """Load metadata from JSON file."""
        if not self.meta_file.exists():
            logger.warning(f"Metadata file not found: {self.meta_file}")
            return
        
        try:
            with open(self.meta_file) as f:
                self.metadata = json.load(f)
            logger.info(f"✓ Metadata loaded from {self.meta_file}")
        except Exception as e:
            logger.error(f"✗ Load failed: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Get all metadata.
        
        Returns:
            Metadata dictionary
        """
        return dict(self.metadata)
