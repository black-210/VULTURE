from typing import Any, Dict, Optional, Tuple

try:
    from sklearn.cluster import KMeans, DBSCAN
except Exception:  # pragma: no cover - optional
    KMeans = DBSCAN = None


def cluster_features(X: Any, method: str = "kmeans", **kwargs) -> Tuple[Any, Optional[Any]]:
    """Cluster feature vectors X using selected method.

    Returns: (labels, model) where model may be None if fallback used.
    """
    if method == "kmeans" and KMeans is not None:
        n_clusters = kwargs.get("n_clusters", 8)
        model = KMeans(n_clusters=n_clusters, random_state=42)
        labels = model.fit_predict(X)
        return labels, model
    if method == "dbscan" and DBSCAN is not None:
        eps = kwargs.get("eps", 0.5)
        model = DBSCAN(eps=eps)
        labels = model.fit_predict(X)
        return labels, model
    # Fallback: simple partition by index
    labels = [i % kwargs.get("n_clusters", 8) for i in range(len(X))]
    return labels, None
