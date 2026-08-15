"""IQ Constellation display."""

import numpy as np
import logging

logger = logging.getLogger(__name__)

class IQConstellation:
    """IQ constellation analysis and visualization."""
    
    def __init__(self):
        self.symbols = []
        self.clusters = None
    
    def plot_constellation(self, iq_data):
        """Prepare constellation data."""
        self.symbols = iq_data.copy()
        return np.real(iq_data), np.imag(iq_data)
    
    def compute_evm(self, iq_data, reference_symbols):
        """Compute Error Vector Magnitude."""
        if len(iq_data) != len(reference_symbols):
            return None
        
        error_vectors = iq_data - reference_symbols
        evm = np.sqrt(np.mean(np.abs(error_vectors)**2))
        evm_db = 20 * np.log10(evm + 1e-10)
        return evm, evm_db
    
    def detect_modulation_order(self):
        """Detect modulation order from constellation."""
        from sklearn.cluster import KMeans
        
        symbols_2d = np.column_stack([np.real(self.symbols), np.imag(self.symbols)])
        
        # Try different cluster numbers
        for n_clusters in [2, 4, 8, 16, 32, 64]:
            kmeans = KMeans(n_clusters=n_clusters, n_init=10)
            kmeans.fit(symbols_2d)
            
            # Check cluster compactness
            silhouette = self._compute_silhouette(symbols_2d, kmeans.labels_)
            if silhouette > 0.7:
                return n_clusters
        
        return 64
    
    @staticmethod
    def _compute_silhouette(X, labels):
        """Simple silhouette score."""
        n_samples = len(X)
        silhouette_vals = []
        
        for i in range(min(n_samples, 100)):
            a = np.mean(np.linalg.norm(X[labels == labels[i]] - X[i], axis=1))
            b = np.mean(np.linalg.norm(X[labels != labels[i]] - X[i], axis=1))
            s = (b - a) / max(a, b) if max(a, b) > 0 else 0
            silhouette_vals.append(s)
        
        return np.mean(silhouette_vals)