"""
Model Hub: simple local model repository with ONNX loader and hash verification.
Stores models under .modelhub/<name> with metadata.
"""
import os
import shutil
import json
import hashlib
from typing import Optional

MODELHUB_DIR = ".modelhub"

class ModelHub:
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.getcwd()
        self.repo_dir = os.path.join(self.base_dir, MODELHUB_DIR)
        os.makedirs(self.repo_dir, exist_ok=True)

    def add_model(self, src_path: str, name: str, metadata: Optional[dict] = None) -> str:
        """Copy model file into hub under given name. Returns dest path."""
        dest_dir = os.path.join(self.repo_dir, name)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, os.path.basename(src_path))
        shutil.copy2(src_path, dest_path)
        meta = metadata or {}
        meta['source'] = src_path
        meta['file'] = os.path.basename(src_path)
        meta_path = os.path.join(dest_dir, 'metadata.json')
        with open(meta_path, 'w') as f:
            json.dump(meta, f)
        return dest_path

    def list_models(self):
        return [d for d in os.listdir(self.repo_dir) if os.path.isdir(os.path.join(self.repo_dir, d))]

    def model_path(self, name: str) -> Optional[str]:
        d = os.path.join(self.repo_dir, name)
        if not os.path.isdir(d):
            return None
        files = [f for f in os.listdir(d) if not f.endswith('.json')]
        return os.path.join(d, files[0]) if files else None

    def verify_hash(self, name: str, expected_sha256: str) -> bool:
        path = self.model_path(name)
        if not path:
            return False
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest() == expected_sha256
