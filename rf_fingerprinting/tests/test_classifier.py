"""Tests for RF classifier."""
import pytest
import numpy as np
from rf_fingerprinting.classifier import RFClassifier


class TestRFClassifier:
    """Test classifier functions."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample training data."""
        np.random.seed(42)
        features_class1 = np.random.randn(50, 20) + np.array([1] * 20)
        features_class2 = np.random.randn(50, 20) + np.array([-1] * 20)
        features = np.vstack([features_class1, features_class2])
        labels = np.hstack([np.zeros(50), np.ones(50)])
        return features, labels
    
    def test_svm_classifier(self, sample_data):
        """Test SVM classifier."""
        features, labels = sample_data
        classifier = RFClassifier(algorithm='svm')
        classifier.fit(features, labels)
        predictions = classifier.predict(features)
        assert len(predictions) == len(labels)
        assert set(predictions) == {0, 1}
    
    def test_rf_classifier(self, sample_data):
        """Test Random Forest classifier."""
        features, labels = sample_data
        classifier = RFClassifier(algorithm='rf')
        classifier.fit(features, labels)
        predictions = classifier.predict(features)
        assert len(predictions) == len(labels)
    
    def test_mlp_classifier(self, sample_data):
        """Test MLP classifier."""
        features, labels = sample_data
        classifier = RFClassifier(algorithm='mlp')
        classifier.fit(features, labels)
        predictions = classifier.predict(features)
        assert len(predictions) == len(labels)
    
    def test_predict_proba(self, sample_data):
        """Test probability predictions."""
        features, labels = sample_data
        classifier = RFClassifier(algorithm='rf')
        classifier.fit(features, labels)
        proba = classifier.predict_proba(features)
        assert proba.shape == (len(labels), 2)
        assert np.all((proba >= 0) & (proba <= 1))
        assert np.allclose(np.sum(proba, axis=1), 1.0)
    
    def test_evaluate(self, sample_data):
        """Test evaluation metrics."""
        features, labels = sample_data
        classifier = RFClassifier(algorithm='rf')
        classifier.fit(features, labels)
        metrics = classifier.evaluate(features, labels)
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1' in metrics
        assert all(0 <= v <= 1 for v in metrics.values())
    
    def test_feature_importance(self, sample_data):
        """Test feature importance (RF only)."""
        features, labels = sample_data
        classifier = RFClassifier(algorithm='rf')
        classifier.fit(features, labels)
        importance = classifier.get_feature_importance()
        assert importance is not None
        assert len(importance) == features.shape[1]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
