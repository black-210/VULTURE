"""Clustering: K-means, DBSCAN, PCA reduction."""

import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class ClusteringEngine:
    """Clustering for device grouping."""

    @staticmethod
    def kmeans_clustering(features: np.ndarray, n_clusters: int = 3) -> Tuple[np.ndarray, np.ndarray]:
        """K-means clustering.
        
        Args:
            features: Feature matrix
            n_clusters: Number of clusters
            
        Returns:
            (cluster_labels, centroids)
        """
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(features)
        logger.info(f"K-means: {n_clusters} clusters, inertia={kmeans.inertia_:.2f}")
        return labels, kmeans.cluster_centers_

    @staticmethod
    def dbscan_clustering(features: np.ndarray, eps: float = 0.5, min_samples: int = 5) -> np.ndarray:
        """DBSCAN clustering.
        
        Args:
            features: Feature matrix
            eps: Epsilon parameter
            min_samples: Minimum samples per cluster
            
        Returns:
            Cluster labels
        """
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(features)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        logger.info(f"DBSCAN: {n_clusters} clusters, {np.sum(labels == -1)} noise points")
        return labels

    @staticmethod
    def pca_reduce(features: np.ndarray, n_components: int = 2) -> Tuple[np.ndarray, PCA]:
        """PCA dimensionality reduction.
        
        Args:
            features: Feature matrix
            n_components: Number of components
            
        Returns:
            (reduced_features, pca_object)
        """
        pca = PCA(n_components=n_components)
        reduced = pca.fit_transform(features)
        variance_ratio = np.sum(pca.explained_variance_ratio_)
        logger.info(f"PCA: {n_components} components, {100*variance_ratio:.1f}% variance")
        return reduced, pca
