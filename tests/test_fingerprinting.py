import pytest
from vulture.fingerprinting.features import extract_fingerprint_features
from vulture.fingerprinting.clustering import cluster_features
from vulture.fingerprinting.classifiers import train_classifier, predict_classifier
from vulture.fingerprinting.anomaly import detect_anomalies


def test_extract_fingerprint_features():
    data = [0, 1, 0, -1, 0, 1]
    feats = extract_fingerprint_features(data, sample_rate=1.0)
    assert "mean" in feats and "spec_centroid" in feats


def test_clustering_fallback():
    X = [[1], [2], [3], [4]]
    labels, model = cluster_features(X, method="kmeans", n_clusters=2)
    assert len(labels) == len(X)


def test_train_predict_dummy():
    X = [[0], [1], [0]]
    y = [0, 1, 0]
    clf = train_classifier(X, y, model_type="rf")
    preds = predict_classifier(clf, X)
    assert len(preds) == len(X)

def test_anomaly_detection():
    X = [[0], [0], [0], [10]]
    out = detect_anomalies(X, contamination=0.25)
    assert "labels" in out
