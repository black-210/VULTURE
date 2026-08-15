"""IQ recording: NPY, BIN, WAV, CSV formats."""

import numpy as np
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class IQRecorder:
    """High-efficiency IQ recording."""

    def __init__(self, filename: str, sample_rate: float, center_freq: float):
        """
        Args:
            filename: Output filename
            sample_rate: Sample rate in Hz
            center_freq: Center frequency in Hz
        """
        self.filename = Path(filename)
        self.sample_rate = sample_rate
        self.center_freq = center_freq
        self.samples = []
        self.metadata = {
            'sample_rate': sample_rate,
            'center_freq': center_freq,
            'num_samples': 0,
        }

    def append_samples(self, samples: np.ndarray) -> None:
        """Append IQ samples.
        
        Args:
            samples: Complex array
        """
        self.samples.append(np.array(samples, dtype=np.complex64))
        self.metadata['num_samples'] += len(samples)

    def save(self, format: str = 'npy') -> None:
        """Save recording.
        
        Args:
            format: 'npy', 'bin', 'wav', 'csv'
        """
        if not self.samples:
            logger.warning("No samples to save")
            return
        
        data = np.concatenate(self.samples)
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if format == 'npy':
                np.save(self.filename, data)
            elif format == 'bin':
                data.astype(np.complex64).tofile(self.filename)
            elif format == 'wav':
                import scipy.io.wavfile as wavfile
                wavfile.write(self.filename, int(self.sample_rate), 
                            (data.real * 32767).astype(np.int16))
            elif format == 'csv':
                np.savetxt(self.filename, np.column_stack([data.real, data.imag]), delimiter=',')
            
            logger.info(f"✓ Saved {len(data)} samples to {self.filename}")
        except Exception as e:
            logger.error(f"✗ Save failed: {e}")
            raise

    def clear(self) -> None:
        """Clear buffer."""
        self.samples = []
        self.metadata['num_samples'] = 0
