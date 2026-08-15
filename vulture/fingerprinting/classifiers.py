from typing import Any, Optional

try:
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
except Exception:  # pragma: no cover - optional
    SVC = RandomForestClassifier = None


def train_classifier(X, y, model_type: str = "rf", **kwargs) -> Any:
    """Train and return a classifier. model_type: 'rf' or 'svm'"""
    if model_type == "rf" and RandomForestClassifier is not None:
        clf = RandomForestClassifier(n_estimators=kwargs.get("n_estimators", 100), random_state=42)
        clf.fit(X, y)
        return clf
    if model_type == "svm" and SVC is not None:
        clf = SVC(probability=True)
        clf.fit(X, y)
        return clf
    # Fallback: simple majority predictor
    class Dummy:
        def __init__(self, majority):
            self.majority = majority
        def predict(self, X):
            return [self.majority for _ in range(len(X))]
    majority = max(set(y), key=list(y).count) if len(y) else None
    return Dummy(majority)


def predict_classifier(model, X):
    if hasattr(model, "predict"):
        return model.predict(X)
    # fallback
    return [None for _ in range(len(X))]
