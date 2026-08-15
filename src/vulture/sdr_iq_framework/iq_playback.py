"""IQ playback with seeking."""

import numpy as np
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class IQPlayback:
    """Efficient IQ playback and streaming."""

    def __init__(self, filename: str):
        """
        Args:
            filename: Input filename
        """
        self.filename = Path(filename)
        self.data = None
        self.position = 0
        self.metadata = {}

    def load(self, format: str = 'npy') -> None:
        """Load recording.
        
        Args:
            format: 'npy', 'bin', 'wav', 'csv'
        """
        if not self.filename.exists():
            raise FileNotFoundError(f"File not found: {self.filename}")
        
        try:
            if format == 'npy':
                self.data = np.load(self.filename)
            elif format == 'bin':
                self.data = np.fromfile(self.filename, dtype=np.complex64)
            elif format == 'csv':
                arr = np.loadtxt(self.filename, delimiter=',')
                self.data = arr[:, 0] + 1j * arr[:, 1]
            elif format == 'wav':
                import scipy.io.wavfile as wavfile
                fs, data = wavfile.read(self.filename)
                self.data = data[:, 0] / 32767.0
            
            self.metadata['num_samples'] = len(self.data)
            logger.info(f"✓ Loaded {len(self.data)} samples from {self.filename}")
        except Exception as e:
            logger.error(f"✗ Load failed: {e}")
            raise

    def read_samples(self, num_samples: int) -> np.ndarray:
        """Read samples from current position.
        
        Args:
            num_samples: Number of samples to read
            
        Returns:
            Complex array
        """
        if self.data is None:
            raise RuntimeError("Data not loaded. Call load() first")
        
        end = min(self.position + num_samples, len(self.data))
        samples = self.data[self.position:end]
        self.position = end
        return samples

    def seek(self, position: int) -> None:
        """Seek to position.
        
        Args:
            position: Sample position
        """
        if self.data is None:
            raise RuntimeError("Data not loaded")
        self.position = max(0, min(position, len(self.data)))

    def get_position(self) -> int:
        """Get current position.
        
        Returns:
            Current sample position
        """
        return self.position
