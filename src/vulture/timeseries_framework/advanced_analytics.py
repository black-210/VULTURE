"""Advanced analytics for time series."""

import numpy as np
from scipy import signal, stats, fftpack
import logging

logger = logging.getLogger(__name__)

class AdvancedAnalytics:
    """Enterprise analytics engine."""
    
    @staticmethod
    def entropy_analysis(data, method='shannon'):
        """Multiple entropy measures."""
        data = np.asarray(data)
        if method == 'shannon':
            hist, _ = np.histogram(np.abs(data), bins=30, density=True)
            hist = hist[hist > 0]
            return -np.sum(hist * np.log2(hist + 1e-10))
        elif method == 'sample':
            m = 2
            N = len(data)
            patterns = {}
            for i in range(N-m):
                pattern = tuple(data[i:i+m])
                patterns[pattern] = patterns.get(pattern, 0) + 1
            se = -sum(p/N * np.log2(p/N + 1e-10) for p in patterns.values())
            return se
        elif method == 'fuzzy':
            return np.mean(np.abs(np.diff(data)))
    
    @staticmethod
    def complexity_analysis(data):
        """Lempel-Ziv complexity."""
        binary = (np.abs(data) > np.median(np.abs(data))).astype(int)
        sequence = ''.join(map(str, binary[:1000]))  # Limit for performance
        complexity = 0
        substring_set = set()
        i = 1
        while i < len(sequence):
            substring = sequence[0:i]
            if substring not in substring_set:
                substring_set.add(substring)
                complexity += 1
            i += 1
        return complexity / len(sequence) if sequence else 0
    
    @staticmethod
    def correlation_dimension(data, embedding_dim=3):
        """Fractal dimension estimation."""
        distances = []
        n = min(1000, len(data))
        data = np.abs(data[:n])
        for i in range(n):
            for j in range(i+1, n):
                dist = np.abs(data[i] - data[j])
                distances.append(dist)
        distances = np.sort(np.array(distances))
        cutoffs = np.logspace(-3, 1, 20)
        dims = []
        for r in cutoffs:
            c_r = np.sum(distances < r)
            if c_r > 0:
                dims.append(np.log(c_r))
        if len(dims) > 1:
            slope = np.polyfit(np.log(cutoffs[:len(dims)]), dims, 1)[0]
            return abs(slope)
        return 0
    
    @staticmethod
    def coherence_analysis(x, y, fs=1e6, nperseg=1024):
        """Cross-spectrum coherence."""
        try:
            f, Cxy = signal.coherence(x, y, fs, nperseg=nperseg)
            return f, Cxy
        except:
            return None, None
    
    @staticmethod
    def phase_synchrony(x, y):
        """Phase locking value."""
        phase_x = np.angle(signal.hilbert(x))
        phase_y = np.angle(signal.hilbert(y))
        phase_diff = np.exp(1j * (phase_x - phase_y))
        plv = np.abs(np.mean(phase_diff))
        return plv
    
    @staticmethod
    def recurrence_analysis(data, embedding_dim=3, threshold=0.5):
        """Recurrence quantification analysis (RQA)."""
        n = len(data)
        rp = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                dist = np.abs(data[i] - data[j])
                if dist < threshold * np.std(data):
                    rp[i, j] = 1
        
        determinism = np.sum(signal.convolve2d(rp, np.ones((2,2)), mode='valid'))
        laminarity = np.sum(np.sum(rp, axis=1)**2) / np.sum(rp)
        
        return {'recurrence_plot': rp, 'determinism': determinism, 'laminarity': laminarity}