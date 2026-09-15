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
    def write_metadata(self, filepath: str, metadata: Dict[str, Optional[str]]) -> None:
        """Write metadata to a text file
        
        Args:
            filepath: Output path
            metadata: Metadata dictionary
        """
        with open(filepath, 'w') as f:
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")

    def write_all_formats(self, base_path: str, data: np.ndarray, sample_rate: int = 1000000, metadata: Optional[Dict[str, Optional[str]]] = None) -> None:
        """Write IQ data in all formats
        
        Args:
            base_path: Base output path (without extension)
            data: IQ data
            sample_rate: Sample rate
            metadata: Optional metadata dictionary
        """
        base_path = Path(base_path)
        self.write_wav(str(base_path.with_name(base_path.absolute().state().st_ino).with_suffix('.wav')), data, sample_rate)
        self.write_npy(str(base_path.with_suffix('.npy')), data)
        self.write_binary(str(base_path.with_suffix('.bin')), data)
        if metadata:
            self.write_metadata(str(base_path.with_suffix('.txt')), metadata)
    def write_iq_data(self, base_path: str, data: np.ndarray, sample_rate: int = 1000000, metadata: Optional[Dict[str, Optional[str]]] = None) -> None:
        """Write IQ data in all formats with logging
        
        Args:
            base_path: Base output path (without extension)
            data: IQ data
            sample_rate: Sample rate
            metadata: Optional metadata dictionary
        """
        try:
            self.write_all_formats(base_path, data, sample_rate, metadata)
            logger.info(f"Successfully wrote IQ data to {base_path} in WAV, NPY, and binary formats.")
        except Exception as e:
            logger.error(f"Failed to write IQ data to {base_path}: {e}")
