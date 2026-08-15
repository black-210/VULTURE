"""Model Trainer: thin wrapper around scikit-learn models for quick prototyping.

Provides a small interface used by CLI and GUI components.
"""
import pickle
from typing import Optional

import numpy as np

try:
    from sklearn.ensemble import RandomForestClassifier
except Exception:  # pragma: no cover - sklearn optional
    RandomForestClassifier = None


class ModelTrainer:
    def __init__(self, model_type: str = 'rf', task: str = 'classification', **kwargs):
        self.model_type = model_type
        self.task = task
        self.model = None
        self.is_trained = False
        self.kwargs = kwargs

    def train(self, X: np.ndarray, y: np.ndarray):
        X = np.asarray(X)
        y = np.asarray(y)
        if self.model_type in ('rf', 'randomforest') and RandomForestClassifier is not None:
            self.model = RandomForestClassifier(n_estimators=self.kwargs.get('n_estimators', 100))
            self.model.fit(X, y)
            self.is_trained = True
            return
        # Fallback: store simple majority predictor
        self.model = {'majority': int(np.round(np.mean(y)))}
        self.is_trained = True

    def predict(self, X: np.ndarray):
        if not self.is_trained:
            raise RuntimeError('Model not trained')
        X = np.asarray(X)
        if hasattr(self.model, 'predict'):
            return self.model.predict(X)
        # fallback majority
        return [self.model.get('majority', 0)] * len(X)

    def save(self, path: str):
        with open(path, 'wb') as fh:
            pickle.dump(self.model, fh)

    def load(self, path: str):
        with open(path, 'rb') as fh:
            self.model = pickle.load(fh)
        self.is_trained = True
