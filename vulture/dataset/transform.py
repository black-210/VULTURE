from typing import Tuple, Any

try:
    from sklearn.model_selection import train_test_split as _sk_split
except Exception:  # pragma: no cover
    _sk_split = None


def train_test_split(dataset: Any, test_size: float = 0.2, random_state: int = 42) -> Tuple[Any, Any]:
    """Simple wrapper for splitting datasets. Falls back to a basic split if sklearn not available."""
    if _sk_split is not None:
        return _sk_split(dataset, test_size=test_size, random_state=random_state)
    # Fallback: naive split assuming indexable dataset
    n = len(dataset)
    split = int(n * (1 - test_size))
    return dataset[:split], dataset[split:]


def clean_missing(dataset: Any, strategy: str = "drop") -> Any:
    """Clean missing values from dataset. strategy: drop | fill_zero"""
    if hasattr(dataset, "dropna") and callable(getattr(dataset, "dropna")):
        if strategy == "drop":
            return dataset.dropna()
        elif strategy == "fill_zero":
            return dataset.fillna(0)
    # Fallback: return dataset unchanged
    return dataset
