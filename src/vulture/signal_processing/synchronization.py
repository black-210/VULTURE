"""Synchronization and timing recovery."""
import numpy as np
from scipy import signal
import logging
logger = logging.getLogger(__name__)
class Synchronization:
    @staticmethod
    def find_sync_pattern(data, pattern, threshold=0.8):
        corr = np.correlate(np.abs(data), np.abs(pattern), mode='same')
        norm_corr = corr / (np.max(corr) + 1e-10)
        peaks = np.where(norm_corr > threshold)[0]
        return peaks
    @staticmethod
    def symbol_timing_recovery(data, samples_per_symbol):
        symbol_stream = data[::samples_per_symbol]
        return symbol_stream
    @staticmethod
    def carrier_recovery_pll(data, estimated_freq):
        t = np.arange(len(data))
        carrier = np.exp(1j * 2 * np.pi * estimated_freq * t)
        return data * np.conj(carrier)
    def get_synchronization_stats(data, pattern):
        """Compute synchronization statistics."""
        peaks = Synchronization.find_sync_pattern(data, pattern)
        return {
            'num_sync_peaks': len(peaks),
            'sync_peak_positions': peaks
        }
    def get_timing_stats(data, samples_per_symbol):
        """Compute timing recovery statistics."""
        symbol_stream = Synchronization.symbol_timing_recovery(data, samples_per_symbol)
        return {
            'num_symbols' : len(symbol_stream),
            'symbol_stream' : symbol_stream
            
        }