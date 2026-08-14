"""Statistical analysis for fingerprinting."""
import numpy as np
from scipy import stats
import logging
logger = logging.getLogger(__name__)
class StatisticalAnalysis:
    @staticmethod
    def compute_statistics(data):
        return {
            'mean': np.mean(data),
            'std': np.std(data),
            'median': np.median(data),
            'var': np.var(data),
            'skewness': stats.skew(data),
            'kurtosis': stats.kurtosis(data),
            'entropy': stats.entropy(np.histogram(data, bins=30)[0]),
        }
    @staticmethod
    def distribution_fit(data):
        from scipy.stats import kstest, normaltest
        _, p_normal = normaltest(data)
        return {'is_normal': p_normal > 0.05}
    @staticmethod
    def correlation_analysis(data1, data2):
        corr = np.corrcoef(data1, data2)[0, 1]
        return corr