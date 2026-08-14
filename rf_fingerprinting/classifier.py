"""RF signal classifiers."""
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from typing import Dict, Tuple, Optional
from utils.logging import setup_logger

logger = setup_logger(__name__)

class RFClassifier:
    """Classify RF signals into known types."""
    
    def __init__(self, algorithm: str = 'rf', random_state: int = 42):
        """Initialize classifier.
        
        Args:
            algorithm: Classification algorithm ('svm', 'rf', or 'mlp').
            random_state: Random seed for reproducibility.
        """
        self.algorithm = algorithm.lower()
        self.random_state = random_state
        self.classifier = None
        self.scaler = StandardScaler()
        self.classes_ = None
    
    def _create_classifier(self):
        """Create classifier based on algorithm choice."""
        if self.algorithm == 'svm':
            return SVC(kernel='rbf', C=1.0, gamma='scale', random_state=self.random_state, probability=True)
        elif self.algorithm == 'rf':
            return RandomForestClassifier(n_estimators=100, max_depth=10, random_state=self.random_state)
        elif self.algorithm == 'mlp':
            return MLPClassifier(hidden_layer_sizes=(128, 64, 32), max_iter=500, random_state=self.random_state)
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
    
    def fit(self, features: np.ndarray, labels: np.ndarray) -> 'RFClassifier':
        """Train classifier.
        
        Args:
            features: Feature matrix (n_samples, n_features).
            labels: Class labels (n_samples,).
        
        Returns:
            Self for chaining.
        """
        # Standardize features
        features_scaled = self.scaler.fit_transform(features)
        
        # Create and fit classifier
        self.classifier = self._create_classifier()
        self.classifier.fit(features_scaled, labels)
        self.classes_ = np.unique(labels)
        
        logger.info(f"{self.algorithm.upper()} classifier trained with {len(self.classes_)} classes")
        return self
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Predict class labels.
        
        Args:
            features: Feature matrix (n_samples, n_features).
        
        Returns:
            Predicted class labels.
        """
        if self.classifier is None:
            raise ValueError("Classifier not fitted yet")
        
        features_scaled = self.scaler.transform(features)
        return self.classifier.predict(features_scaled)
    
    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        """Predict class probabilities.
        
        Args:
            features: Feature matrix (n_samples, n_features).
        
        Returns:
            Class probabilities (n_samples, n_classes).
        """
        if self.classifier is None:
            raise ValueError("Classifier not fitted yet")
        
        features_scaled = self.scaler.transform(features)
        
        if hasattr(self.classifier, 'predict_proba'):
            return self.classifier.predict_proba(features_scaled)
        else:
            # For SVM without probability estimates
            return np.ones((len(features), len(self.classes_))) / len(self.classes_)
    
    def evaluate(self, features: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
        """Evaluate classifier performance.
        
        Args:
            features: Feature matrix.
            labels: True labels.
        
        Returns:
            Dictionary of metrics.
        """
        predictions = self.predict(features)
        
        metrics = {
            'accuracy': accuracy_score(labels, predictions),
            'precision': precision_score(labels, predictions, average='weighted', zero_division=0),
            'recall': recall_score(labels, predictions, average='weighted', zero_division=0),
            'f1': f1_score(labels, predictions, average='weighted', zero_division=0),
        }
        
        return metrics
    
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """Get feature importance (Random Forest only).
        
        Returns:
            Feature importance scores or None.
        """
        if self.algorithm == 'rf' and hasattr(self.classifier, 'feature_importances_'):
            return self.classifier.feature_importances_
        return None
