from typing import Any, Optional

try:
    from sklearn.base import BaseEstimator
except Exception:
    BaseEstimator = object  # type: ignore

class Trainer:
    """Simple training wrapper that supports sklearn estimators.

    For deep learning models, extend this class or implement a PyTorchTrainer.
    """
    def __init__(self, model: Any):
        self.model = model

    def fit(self, X, y, **kwargs) -> Any:
        if hasattr(self.model, "fit"):
            return self.model.fit(X, y, **kwargs)
        raise RuntimeError("Model does not support fit()")

    def predict(self, X) -> Any:
        if hasattr(self.model, "predict"):
            return self.model.predict(X)
        raise RuntimeError("Model does not support predict()")

    def save(self, path: str) -> None:
        try:
            import joblib
            joblib.dump(self.model, path)
        except Exception:
            # fallback: try pickle
            import pickle
            with open(path, "wb") as f:
                pickle.dump(self.model, f)

    def load(self, path: str) -> Any:
        try:
            import joblib
            self.model = joblib.load(path)
            return self.model
        except Exception:
            import pickle
            with open(path, "rb") as f:
                self.model = pickle.load(f)
            return self.model
