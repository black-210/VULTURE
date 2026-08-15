from typing import Optional, Tuple
import os

try:
    import pandas as pd
except Exception:  # pragma: no cover - optional dependency
    pd = None

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None


def load_csv(path: str, **kwargs) -> Optional[object]:
    if pd is None:
        raise RuntimeError("pandas is required to load CSV files")
    return pd.read_csv(path, **kwargs)


def load_json(path: str, **kwargs) -> Optional[object]:
    if pd is None:
        raise RuntimeError("pandas is required to load JSON files")
    return pd.read_json(path, **kwargs)


def load_npy(path: str) -> Optional[object]:
    if np is None:
        raise RuntimeError("numpy is required to load NPY files")
    return np.load(path)


def load_parquet(path: str, **kwargs) -> Optional[object]:
    if pd is None:
        raise RuntimeError("pandas is required to load Parquet files")
    return pd.read_parquet(path, **kwargs)
