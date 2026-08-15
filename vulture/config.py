import json
from pathlib import Path

DEFAULT_CONFIG = {"setting_a": True, "setting_b": "value"}


def load_config(path=None):
    if path:
        p = Path(path)
        if p.exists():
            with p.open() as f:
                return json.load(f)
    return DEFAULT_CONFIG.copy()
