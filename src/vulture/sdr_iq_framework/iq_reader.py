"""IQ Reader - Multi-format IQ Data Loading"""
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict
import logging

logger = logging.getLogger(__name__)

class IQReader:
    """Read IQ data from multiple formats"""
    
    SUPPORTED_FORMATS = ['.wav', '.npy', '.npz', '.bin', '.raw', '.sigmf']
    
    def read_wav(self, filepath: str, start: int = 0, length: Optional[int] = None) -> Tuple[np.ndarray, int]:
        """Read WAV IQ file
        
        Args:
            filepath: Path to WAV file
            start: Start sample
            length: Number of samples
        
        Returns:
            (IQ data, sample rate)
        """
        import scipy.io.wavfile as wavfile
        sr, data = wavfile.read(filepath)
        
        if data.dtype != np.complex64 and data.dtype != np.complex128:
            if len(data.shape) == 2:
                data = data[:, 0] + 1j * data[:, 1]
            elif len(data.shape) == 1:
                data = data.astype(np.complex64)
        
        if length is None:
            return data[start:], sr
        return data[start:start+length], sr
    
    def read_npy(self, filepath: str) -> np.ndarray:
        """Read NPY file
        
        Args:
            filepath: Path to NPY file
        
        Returns:
            IQ data
        """
        return np.load(filepath)
    
    def read_binary(self, filepath: str, dtype: str = 'complex64',
                   sample_rate: float = 1e6) -> Tuple[np.ndarray, float]:
        """Read raw binary IQ file
        
        Args:
            filepath: Path to binary file
            dtype: Data type
            sample_rate: Sample rate
        
        Returns:
            (IQ data, sample rate)
        """
        data = np.fromfile(filepath, dtype=dtype)
        return data, sample_rate
    
    def detect_and_read(self, filepath: str) -> Tuple[np.ndarray, Dict]:
        """Auto-detect format and read
        
        Args:
            filepath: Path to file
        
        Returns:
            (IQ data, metadata)
        """
        path = Path(filepath)
        suffix = path.suffix.lower()
        
        metadata = {'format': suffix, 'filepath': str(path)}
        
        if suffix == '.wav':
            data, sr = self.read_wav(filepath)
            metadata['sample_rate'] = sr
        elif suffix == '.npy':
            data = self.read_npy(filepath)
        elif suffix in ['.bin', '.raw']:
            data, sr = self.read_binary(filepath)
            metadata['sample_rate'] = sr
        else:
            raise ValueError(f"Unsupported format: {suffix}")
        
        return data, metadata
