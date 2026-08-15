"""Device classification: SVM, RF, MLP."""

import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class DeviceClassifier:
    """RF device identification classifier."""

    def __init__(self, model_type: str = 'svm'):
        """
        Args:
            model_type: 'svm', 'rf', 'mlp'
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
        if model_type == 'svm':
            self.model = SVC(kernel='rbf', probability=True)
        elif model_type == 'rf':
            self.model = RandomForestClassifier(n_estimators=100)
        elif model_type == 'mlp':
            self.model = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=1000)
        else:
            raise ValueError(f"Unknown model: {model_type}")

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train classifier.
        
        Args:
            X: Feature matrix
            y: Device labels
        """
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        logger.info(f"✓ Trained {self.model_type} device classifier")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict device class.
        
        Args:
            X: Feature matrix
            
        Returns:
            Device class predictions
        """
        if not self.is_trained:
            raise RuntimeError("Model not trained")
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get prediction probabilities.
        
        Args:
            X: Feature matrix
            
        Returns:
            Class probabilities
        """
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)

    def get_accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute accuracy.
        
        Args:
            X: Feature matrix
            y: True labels
            
        Returns:
            Accuracy score
        """
        predictions = self.predict(X)
        return np.mean(predictions == y)
