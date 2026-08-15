"""Waterfall display buffer with statistics and efficient memory management."""

import numpy as np
from typing import Tuple
import logging
from collections import deque

logger = logging.getLogger(__name__)


class WaterfallBuffer:
    """Efficient waterfall/spectrogram accumulation."""

    def __init__(self, num_rows: int, num_cols: int, dtype: str = 'float32'):
        """Initialize buffer.
        
        Args:
            num_rows: Number of time frames to keep
            num_cols: Number of frequency bins
            dtype: Data type
        """
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.dtype = dtype
        self.buffer = deque(maxlen=num_rows)
        self.frame_count = 0

    def append_frame(self, frame: np.ndarray) -> None:
        """Add spectrogram frame.
        
        Args:
            frame: Frequency-domain data (1D array)
        """
        if len(frame) != self.num_cols:
            raise ValueError(f"Frame size {len(frame)} != {self.num_cols}")
        self.buffer.append(frame.astype(self.dtype))
        self.frame_count += 1

    def get_waterfall(self) -> np.ndarray:
        """Get 2D waterfall (time x frequency).
        
        Returns:
            2D array of accumulated frames
        """
        if not self.buffer:
            return np.zeros((0, self.num_cols), dtype=self.dtype)
        return np.array(list(self.buffer))

    def get_statistics(self) -> Dict:
        """Get buffer statistics.
        
        Returns:
            Dict with min, max, mean, std
        """
        waterfall = self.get_waterfall()
        if len(waterfall) == 0:
            return {'min': 0, 'max': 0, 'mean': 0, 'std': 0}
        return {
            'min': np.min(waterfall),
            'max': np.max(waterfall),
            'mean': np.mean(waterfall),
            'std': np.std(waterfall),
            'num_frames': len(self.buffer),
        }

    def clear(self) -> None:
        """Clear buffer."""
        self.buffer.clear()
        logger.info("Waterfall buffer cleared")
