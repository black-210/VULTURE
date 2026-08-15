from typing import Any, Dict

try:
    from sklearn.metrics import accuracy_score, precision_score, recall_score
except Exception:  # pragma: no cover - optional
    accuracy_score = precision_score = recall_score = None


def compute_metrics(y_true, y_pred) -> Dict[str, float]:
    """Compute basic classification metrics. Falls back to simple implementations if sklearn is missing."""
    if accuracy_score is not None:
        return {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred, zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        }
    # fallback naive accuracy
    total = len(y_true)
    correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return {"accuracy": correct / total if total else 0.0}
