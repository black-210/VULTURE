"""Waterfall display for RF visualization."""
import numpy as np
import logging

logger = logging.getLogger(__name__)

class WaterfallDisplay:
    """Waterfall display methods."""
    
    def __init__(self, max_rows=1000):
        self.max_rows = max_rows
        self.data = []
    
    def add_row(self, spectrum):
        self.data.append(spectrum)
        if len(self.data) > self.max_rows:
            self.data.pop(0)
    
    def get_waterfall_data(self):
        return np.array(self.data)
    
    def clear(self):
        self.data = []
    
    def get_stats(self):
        if len(self.data) == 0:
            return {}
        data = np.array(self.data)
        return {
            'rows': len(self.data),
            'mean_power': np.mean(data),
            'max_power': np.max(data),
            'min_power': np.min(data),
        }