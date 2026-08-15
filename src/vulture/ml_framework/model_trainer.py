"""Model training: RF, SVM, MLP."""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler
from typing import Optional
import logging
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Model training for classification and regression."""

    def __init__(self, model_type: str = 'rf', task: str = 'classification',
                 **kwargs):
        """
        Args:
            model_type: 'rf', 'svm', 'mlp'
            task: 'classification' or 'regression'
            **kwargs: Model-specific hyperparameters
        """
        self.model_type = model_type
        self.task = task
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
        if model_type == 'rf':
            if task == 'classification':
                self.model = RandomForestClassifier(**kwargs)
            else:
                self.model = RandomForestRegressor(**kwargs)
        elif model_type == 'svm':
            if task == 'classification':
                self.model = SVC(**kwargs)
            else:
                self.model = SVR(**kwargs)
        elif model_type == 'mlp':
            if task == 'classification':
                self.model = MLPClassifier(hidden_layer_sizes=(100, 50), **kwargs)
            else:
                self.model = MLPRegressor(hidden_layer_sizes=(100, 50), **kwargs)
        else:
            raise ValueError(f"Unknown model type: {model_type}")

    def train(self, X: np.ndarray, y: np.ndarray, normalize: bool = True) -> None:
        """Train model.
        
        Args:
            X: Features
            y: Labels
            normalize: Whether to normalize features
        """
        if normalize:
            X = self.scaler.fit_transform(X)
        
        self.model.fit(X, y)
        self.is_trained = True
        logger.info(f"✓ Trained {self.model_type} {self.task} model")

    def predict(self, X: np.ndarray, normalize: bool = True) -> np.ndarray:
        """Make predictions.
        
        Args:
            X: Features
            normalize: Whether to normalize features
            
        Returns:
            Predictions
        """
        if not self.is_trained:
            raise RuntimeError("Model not trained")
        
        if normalize:
            X = self.scaler.transform(X)
        
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray, normalize: bool = True) -> np.ndarray:
        """Get prediction probabilities (classification only).
        
        Args:
            X: Features
            normalize: Whether to normalize features
            
        Returns:
            Class probabilities
        """
        if self.task != 'classification':
            raise RuntimeError("predict_proba only for classification")
        
        if normalize:
            X = self.scaler.transform(X)
        
        return self.model.predict_proba(X)

    def save(self, path: str) -> None:
        """Save model to disk.
        
        Args:
            path: Output path
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, 'wb') as f:
            pickle.dump((self.model, self.scaler), f)
        logger.info(f"✓ Saved model to {path}")

    def load(self, path: str) -> None:
        """Load model from disk.
        
        Args:
            path: Model path
        """
        with open(path, 'rb') as f:
            self.model, self.scaler = pickle.load(f)
        self.is_trained = True
        logger.info(f"✓ Loaded model from {path}")
