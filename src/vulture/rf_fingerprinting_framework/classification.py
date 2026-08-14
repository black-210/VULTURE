"""Classification for device identification."""
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import numpy as np
import logging
logger = logging.getLogger(__name__)
class Classification:
    def __init__(self, model_type='svm'):
        if model_type == 'svm':
            self.model = SVC(kernel='rbf')
        elif model_type == 'rf':
            self.model = RandomForestClassifier()
        elif model_type == 'mlp':
            self.model = MLPClassifier()
    def train(self, X, y):
        self.model.fit(X, y)
    def predict(self, X):
        return self.model.predict(X)
    def get_accuracy(self, X, y):
        return self.model.score(X, y)