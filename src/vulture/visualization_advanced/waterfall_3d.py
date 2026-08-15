"""3D Waterfall visualization."""

import numpy as np
import logging

logger = logging.getLogger(__name__)

class Waterfall3D:
    """3D waterfall display for time-frequency evolution."""
    
    def __init__(self, max_frames=100):
        self.max_frames = max_frames
        self.frames = []
        self.timestamps = []
    
    def add_frame(self, spectrum, timestamp=None):
        """Add spectrum frame."""
        self.frames.append(spectrum)
        self.timestamps.append(timestamp or len(self.frames))
        
        if len(self.frames) > self.max_frames:
            self.frames.pop(0)
            self.timestamps.pop(0)
    
    def get_waterfall_matrix(self):
        """Get matrix for 3D visualization."""
        if not self.frames:
            return None
        return np.array(self.frames)
    
    def get_colormap_data(self):
        """Get data for colormap rendering."""
        matrix = self.get_waterfall_matrix()
        if matrix is None:
            return None
        return np.clip(matrix, -100, 0)  # Normalized to dB range
    
    def compute_occupancy_map(self):
        """Compute time-frequency occupancy."""
        matrix = self.get_waterfall_matrix()
        if matrix is None:
            return None
        threshold = np.mean(matrix) + np.std(matrix)
        occupancy = (matrix > threshold).astype(float)
        return np.mean(occupancy, axis=0)  # Frequency-domain occupancy