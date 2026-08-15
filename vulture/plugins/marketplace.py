"""
Plugin marketplace and registry (MVP).
Plugins are described by a JSON metadata file and can be registered in the marketplace.
"""
import os
import json
from typing import Dict, List, Optional

MARKETPLACE_DIR = '.plugins'

class PluginMarketplace:
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.getcwd()
        self.dir = os.path.join(self.base_dir, MARKETPLACE_DIR)
        os.makedirs(self.dir, exist_ok=True)

    def register_plugin(self, plugin_dir: str) -> Optional[str]:
        """Register a plugin given its directory containing metadata.json. Returns plugin id."""
        meta_path = os.path.join(plugin_dir, 'metadata.json')
        if not os.path.exists(meta_path):
            return None
        with open(meta_path, 'r') as f:
            meta = json.load(f)
        pid = meta.get('id') or meta.get('name')
        if not pid:
            return None
        dest = os.path.join(self.dir, pid)
        if os.path.exists(dest):
            # update metadata
            pass
        else:
            os.makedirs(dest, exist_ok=True)
        # copy metadata only for MVP
        with open(os.path.join(dest, 'metadata.json'), 'w') as f:
            json.dump(meta, f)
        return pid

    def list_plugins(self) -> List[str]:
        return [d for d in os.listdir(self.dir) if os.path.isdir(os.path.join(self.dir, d))]

    def get_metadata(self, plugin_id: str) -> Optional[Dict]:
        p = os.path.join(self.dir, plugin_id, 'metadata.json')
        if not os.path.exists(p):
            return None
        with open(p, 'r') as f:
            return json.load(f)
