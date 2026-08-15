from typing import Any, Dict, List


def validate_schema(dataset: Any, schema: Dict[str, Any]) -> List[str]:
    """Validate a dataset against a simple schema.

    Schema format (example): {"col1": "float", "col2": "int", "col3": "str"}
    Returns a list of error messages (empty if valid).
    """
    errors = []
    # Basic duck-typed validation for pandas-like objects
    if hasattr(dataset, "columns"):
        cols = set(dataset.columns)
        for col, coltype in schema.items():
            if col not in cols:
                errors.append(f"Missing column: {col}")
            # further type checks could be implemented
    else:
        errors.append("Unsupported dataset object for schema validation")
    return errors
