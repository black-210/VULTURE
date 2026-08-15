"""Statistical analysis: Distribution fitting, correlation."""

import numpy as np
from scipy import stats
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class StatisticalAnalyzer:
    """Statistical analysis for device fingerprinting."""

    @staticmethod
    def fit_distributions(data: np.ndarray, distributions: list = None) -> Dict:
        """Fit probability distributions.
        
        Args:
            data: Input data
            distributions: List of distribution names
            
        Returns:
            Dict with fitted parameters
        """
        if distributions is None:
            distributions = ['norm', 'gamma', 'lognorm', 'expon']
        
        results = {}
        for dist_name in distributions:
            try:
                dist = getattr(stats, dist_name)
                params = dist.fit(data)
                results[dist_name] = {'params': params, 'ks_test': stats.kstest(data, lambda x: dist.cdf(x, *params))}
            except Exception as e:
                logger.debug(f"Failed to fit {dist_name}: {e}")
        
        return results

    @staticmethod
    def compute_correlation_matrix(feature_matrix: np.ndarray) -> np.ndarray:
        """Compute feature correlation matrix.
        
        Args:
            feature_matrix: Feature matrix (n_samples, n_features)
            
        Returns:
            Correlation matrix
        """
        return np.corrcoef(feature_matrix.T)

    @staticmethod
    def compute_covariance_matrix(feature_matrix: np.ndarray) -> np.ndarray:
        """Compute feature covariance matrix.
        
        Args:
            feature_matrix: Feature matrix
            
        Returns:
            Covariance matrix
        """
        return np.cov(feature_matrix.T)

    @staticmethod
    def mahalanobis_distance(x: np.ndarray, mean: np.ndarray, cov: np.ndarray) -> float:
        """Compute Mahalanobis distance.
        
        Args:
            x: Point
            mean: Mean vector
            cov: Covariance matrix
            
        Returns:
            Mahalanobis distance
        """
        diff = x - mean
        cov_inv = np.linalg.pinv(cov)
        return np.sqrt(np.dot(np.dot(diff, cov_inv), diff))
