"""Model training framework."""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import logging
logger = logging.getLogger(__name__)
class ModelTrainer:
    def __init__(self, model_type='rf'):
        if model_type == 'rf':
            self.model = RandomForestClassifier(n_estimators=100)
        elif model_type == 'svm':
            self.model = SVC(kernel='rbf')
        elif model_type == 'mlp':
            self.model = MLPClassifier(hidden_layer_sizes=(100, 50))
        self.is_trained = False
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        self.is_trained = True
        logger.info("Model trained successfully")
    def predict(self, X_test):
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        return self.model.predict(X_test)
    def get_feature_importance(self):
        if hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        return None