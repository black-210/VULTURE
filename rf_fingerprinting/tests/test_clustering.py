"""Tests for clustering."""
import pytest
import numpy as np
from rf_fingerprinting.clustering import Clusterer


class TestClusterer:
    """Test clustering functions."""
    
    @pytest.fixture
    def sample_features(self):
        """Create sample feature data."""
        np.random.seed(42)
        cluster1 = np.random.randn(30, 10) + np.array([2, 2, 2, 2, 2, 0, 0, 0, 0, 0])
        cluster2 = np.random.randn(30, 10) + np.array([-2, -2, -2, -2, -2, 0, 0, 0, 0, 0])
        return np.vstack([cluster1, cluster2])
    
    def test_kmeans_fit(self, sample_features):
        """Test K-means clustering."""
        clusterer = Clusterer(algorithm='kmeans', n_clusters=2)
        clusterer.fit(sample_features)
        labels = clusterer.predict(sample_features)
        assert len(labels) == len(sample_features)
        assert len(np.unique(labels)) <= 2
    
    def test_dbscan_fit(self, sample_features):
        """Test DBSCAN clustering."""
        clusterer = Clusterer(algorithm='dbscan')
        clusterer.fit(sample_features)
        labels = clusterer.predict(sample_features)
        assert len(labels) == len(sample_features)
    
    def test_get_cluster_centers(self, sample_features):
        """Test getting cluster centers."""
        clusterer = Clusterer(algorithm='kmeans', n_clusters=2)
        clusterer.fit(sample_features)
        centers = clusterer.get_cluster_centers()
        assert centers is not None
        assert centers.shape[0] == 2
    
    def test_silhouette_score(self, sample_features):
        """Test silhouette score computation."""
        clusterer = Clusterer(algorithm='kmeans', n_clusters=2)
        clusterer.fit(sample_features)
        score = clusterer.get_silhouette_score(sample_features)
        assert -1 <= score <= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
