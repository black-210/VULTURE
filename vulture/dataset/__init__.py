"""
Dataset Intelligence framework package.
Support for multi-format loading, profiling, validation, and transformations.
"""
from .io import load_csv, load_json, load_npy, load_parquet
from .validate import validate_schema
from .transform import train_test_split, clean_missing

__all__ = [
    "load_csv",
    "load_json",
    "load_npy",
    "load_parquet",
    "validate_schema",
    "train_test_split",
    "clean_missing",
]
