"""Clustering for device grouping."""
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
import numpy as np
import logging
logger = logging.getLogger(__name__)
class Clustering:
    @staticmethod
    def kmeans(data, n_clusters=5):
        kmeans = KMeans(n_clusters=n_clusters)
        labels = kmeans.fit_predict(data)
        return labels, kmeans.cluster_centers_
    @staticmethod
    def dbscan(data, eps=0.5, min_samples=5):
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(data)
        return labels
    @staticmethod
    def pca_reduction(data, n_components=2):
        pca = PCA(n_components=n_components)
        reduced = pca.fit_transform(data)
        return reduced, pca