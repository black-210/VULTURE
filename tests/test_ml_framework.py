"""Tests for ML Framework."""
import pytest
import numpy as np
from vulture.ml_framework import Preprocessing, FeatureEngineering, ModelTrainer, ModelEvaluation

class TestPreprocessing:
    def test_normalization(self):
        data = np.array([1, 2, 3, 4, 5])
        normalized = Preprocessing.normalize(data, method='standard')
        assert np.abs(np.mean(normalized)) < 1e-10
        assert np.abs(np.std(normalized) - 1.0) < 1e-10

class TestFeatureEngineering:
    def test_statistical_features(self):
        data = np.sin(2 * np.pi * 0.1 * np.arange(1000))
        features = FeatureEngineering.extract_statistical_features(data)
        assert 'mean' in features
        assert 'std' in features
        assert 'skewness' in features

class TestModelTrainer:
    def test_model_training(self):
        X_train = np.random.rand(100, 10)
        y_train = np.random.randint(0, 2, 100)
        trainer = ModelTrainer('rf')
        trainer.train(X_train, y_train)
        assert trainer.is_trained
        X_test = np.random.rand(10, 10)
        predictions = trainer.predict(X_test)
        assert len(predictions) == 10
