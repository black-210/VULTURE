"""Dataset intelligence: schema detection and profiling helpers."""
from typing import Any, Dict, List


def detect_schema(sample_rows: List[Dict[str, Any]]) -> Dict[str, str]:
    # very lightweight: infer types from first row
    if not sample_rows:
        return {}
    first = sample_rows[0]
    schema = {}
    for k, v in first.items():
        schema[k] = type(v).__name__
    return schema
