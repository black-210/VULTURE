"""IQ Writer - Save IQ Data in Multiple Formats"""
import numpy as np
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class IQWriter:
    """Write IQ data to multiple formats"""
    
    def write_wav(self, filepath: str, data: np.ndarray, sample_rate: int = 1000000) -> None:
        """Write WAV IQ file
        
        Args:
            filepath: Output path
            data: IQ data
            sample_rate: Sample rate
        """
        import scipy.io.wavfile as wavfile
        if np.iscomplexobj(data):
            stereo_data = np.stack([np.real(data), np.imag(data)], axis=1).astype(np.int16)
        else:
            stereo_data = data.astype(np.int16)
        wavfile.write(filepath, sample_rate, stereo_data)
    
    def write_npy(self, filepath: str, data: np.ndarray) -> None:
        """Write NPY file
        
        Args:
            filepath: Output path
            data: IQ data
        """
        np.save(filepath, data)
    
    def write_binary(self, filepath: str, data: np.ndarray, dtype: str = 'complex64') -> None:
        """Write raw binary IQ file
        
        Args:
            filepath: Output path
            data: IQ data
            dtype: Data type
        """
        data.astype(dtype).tofile(filepath)
