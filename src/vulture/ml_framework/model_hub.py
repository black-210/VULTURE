"""Model hub: Local repository, persistence, discovery."""

import json
import hashlib
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ModelHub:
    """Local model repository and management."""

    def __init__(self, hub_path: str = './models'):
        """
        Args:
            hub_path: Path to model hub directory
        """
        self.hub_path = Path(hub_path)
        self.hub_path.mkdir(parents=True, exist_ok=True)
        self.metadata = {}

    def register_model(self, name: str, model_path: str, description: str,
                      tags: list = None, version: str = '1.0.0') -> None:
        """Register model in hub.
        
        Args:
            name: Model name
            model_path: Path to model file
            description: Model description
            tags: Optional tags
            version: Model version
        """
        model_file = self.hub_path / name / f'v{version}' / 'model.pkl'
        model_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Compute hash
        with open(model_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        metadata = {
            'name': name,
            'version': version,
            'description': description,
            'tags': tags or [],
            'hash': file_hash,
            'model_file': str(model_file),
        }
        
        meta_file = model_file.parent / 'metadata.json'
        with open(meta_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"✓ Registered model: {name} v{version}")

    def list_models(self) -> Dict[str, list]:
        """List all models in hub.
        
        Returns:
            Dict of model_name -> versions
        """
        models = {}
        for model_dir in self.hub_path.iterdir():
            if model_dir.is_dir():
                versions = [v.name for v in model_dir.iterdir() if v.is_dir()]
                models[model_dir.name] = sorted(versions)
        return models

    def get_metadata(self, name: str, version: str = 'latest') -> Dict:
        """Get model metadata.
        
        Args:
            name: Model name
            version: Model version (or 'latest')
            
        Returns:
            Metadata dict
        """
        model_path = self.hub_path / name
        if not model_path.exists():
            raise FileNotFoundError(f"Model '{name}' not found")
        
        if version == 'latest':
            versions = sorted([v.name for v in model_path.iterdir() if v.is_dir()])
            version = versions[-1] if versions else 'v1.0.0'
        
        meta_file = model_path / version / 'metadata.json'
        with open(meta_file) as f:
            return json.load(f)

    def search(self, query: str) -> Dict:
        """Search models by name or tags.
        
        Args:
            query: Search query
            
        Returns:
            Matching models
        """
        results = {}
        for model_dir in self.hub_path.iterdir():
            if query.lower() in model_dir.name.lower():
                results[model_dir.name] = [v.name for v in model_dir.iterdir() if v.is_dir()]
        return results
