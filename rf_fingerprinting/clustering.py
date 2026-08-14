"""Clustering algorithms for RF signal grouping."""
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Optional
from utils.logging import setup_logger

logger = setup_logger(__name__)

class Clusterer:
    """Cluster RF signals into groups based on features."""
    
    def __init__(self, algorithm: str = 'kmeans', n_clusters: int = 5):
        """Initialize clusterer.
        
        Args:
            algorithm: Clustering algorithm ('kmeans' or 'dbscan').
            n_clusters: Number of clusters (for k-means).
        """
        self.algorithm = algorithm.lower()
        self.n_clusters = n_clusters
        self.clusterer = None
        self.scaler = StandardScaler()
    
    def fit(self, features: np.ndarray) -> 'Clusterer':
        """Fit clustering model.
        
        Args:
            features: Feature matrix (n_samples, n_features).
        
        Returns:
            Self for chaining.
        """
        # Standardize features
        features_scaled = self.scaler.fit_transform(features)
        
        if self.algorithm == 'kmeans':
            self.clusterer = KMeans(
                n_clusters=self.n_clusters,
                random_state=42,
                n_init=10,
            )
            self.clusterer.fit(features_scaled)
            logger.info(f"KMeans fitted with {self.n_clusters} clusters")
        
        elif self.algorithm == 'dbscan':
            self.clusterer = DBSCAN(eps=0.5, min_samples=5)
            self.clusterer.fit(features_scaled)
            n_clusters = len(set(self.clusterer.labels_)) - (1 if -1 in self.clusterer.labels_ else 0)
            logger.info(f"DBSCAN found {n_clusters} clusters")
        
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
        
        return self
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Predict cluster labels.
        
        Args:
            features: Feature matrix (n_samples, n_features).
        
        Returns:
            Cluster labels.
        """
        if self.clusterer is None:
            raise ValueError("Clusterer not fitted yet")
        
        features_scaled = self.scaler.transform(features)
        return self.clusterer.predict(features_scaled)
    
    def get_cluster_centers(self) -> Optional[np.ndarray]:
        """Get cluster centers (k-means only).
        
        Returns:
            Cluster centers or None if using DBSCAN.
        """
        if self.algorithm == 'kmeans' and hasattr(self.clusterer, 'cluster_centers_'):
            return self.scaler.inverse_transform(self.clusterer.cluster_centers_)
        return None
    
    def get_silhouette_score(self, features: np.ndarray) -> float:
        """Compute silhouette score.
        
        Args:
            features: Feature matrix.
        
        Returns:
            Silhouette score.
        """
        from sklearn.metrics import silhouette_score
        
        if self.clusterer is None:
            raise ValueError("Clusterer not fitted yet")
        
        features_scaled = self.scaler.transform(features)
        labels = self.predict(features)
        return silhouette_score(features_scaled, labels)
