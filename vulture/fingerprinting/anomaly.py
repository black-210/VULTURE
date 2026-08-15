from typing import Any, Dict, Optional

try:
    from sklearn.ensemble import IsolationForest
except Exception:  # pragma: no cover - optional
    IsolationForest = None


def detect_anomalies(X, contamination: float = 0.01) -> Dict[str, Any]:
    """Detect anomalies in feature matrix X. Returns dict with labels and model info."""
    if IsolationForest is not None:
        model = IsolationForest(contamination=contamination, random_state=42)
        model.fit(X)
        preds = model.predict(X)  # -1 for outliers, 1 for inliers
        labels = [1 if p == -1 else 0 for p in preds]
        return {"labels": labels, "model": model}
    # Fallback: no anomalies detected
    return {"labels": [0 for _ in range(len(X))], "model": None}
