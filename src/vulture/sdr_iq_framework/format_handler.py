"""Format auto-detection and conversion."""

import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class FormatHandler:
    """Unified format handling and conversion."""

    SUPPORTED_FORMATS = ['npy', 'bin', 'wav', 'csv', 'sigmf']

    @staticmethod
    def detect_format(filename: str) -> str:
        """Auto-detect file format.
        
        Args:
            filename: Input filename
            
        Returns:
            Detected format
        """
        p = Path(filename)
        suffix = p.suffix.lower().strip('.')
        
        if suffix in FormatHandler.SUPPORTED_FORMATS:
            return suffix
        raise ValueError(f"Unknown format: {suffix}")

    @staticmethod
    def load(filename: str, format: Optional[str] = None) -> Tuple[np.ndarray, Dict]:
        """Load data from file.
        
        Args:
            filename: Input file
            format: Format (auto-detect if None)
            
        Returns:
            (data, metadata_dict)
        """
        if format is None:
            format = FormatHandler.detect_format(filename)
        
        p = Path(filename)
        metadata = {'format': format, 'filename': str(p)}
        
        try:
            if format == 'npy':
                data = np.load(filename)
            elif format == 'bin':
                data = np.fromfile(filename, dtype=np.complex64)
            elif format == 'csv':
                arr = np.loadtxt(filename, delimiter=',')
                data = arr[:, 0] + 1j * arr[:, 1] if arr.ndim > 1 else arr
            elif format == 'wav':
                import scipy.io.wavfile as wavfile
                fs, wav_data = wavfile.read(filename)
                data = wav_data.astype(np.float32) / 32767.0
                metadata['sample_rate'] = fs
            elif format == 'sigmf':
                # SigMF: metadata.json + data.sigmf-data
                import json
                meta_file = p.with_suffix('.sigmf-meta')
                if meta_file.exists():
                    with open(meta_file) as f:
                        metadata.update(json.load(f))
                data = np.fromfile(p.with_suffix('.sigmf-data'), dtype=np.complex64)
            
            metadata['num_samples'] = len(data)
            logger.info(f"✓ Loaded {len(data)} samples ({format})")
            return data, metadata
        except Exception as e:
            logger.error(f"✗ Load failed: {e}")
            raise

    @staticmethod
    def save(data: np.ndarray, filename: str, format: str = 'npy', 
            metadata: Dict = None) -> None:
        """Save data to file.
        
        Args:
            data: Complex or real array
            filename: Output filename
            format: Output format
            metadata: Optional metadata dict
        """
        p = Path(filename)
        p.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if format == 'npy':
                np.save(filename, data)
            elif format == 'bin':
                data.astype(np.complex64).tofile(filename)
            elif format == 'csv':
                if np.iscomplexobj(data):
                    arr = np.column_stack([data.real, data.imag])
                else:
                    arr = data
                np.savetxt(filename, arr, delimiter=',')
            elif format == 'sigmf':
                import json
                np.array(data, dtype=np.complex64).tofile(p.with_suffix('.sigmf-data'))
                meta = {'datatype': 'cf32_le', 'num_samples': len(data)}
                meta.update(metadata or {})
                with open(p.with_suffix('.sigmf-meta'), 'w') as f:
                    json.dump(meta, f, indent=2)
            
            logger.info(f"✓ Saved {len(data)} samples ({format})")
        except Exception as e:
            logger.error(f"✗ Save failed: {e}")
            raise

    @staticmethod
    def convert(input_file: str, output_file: str, output_format: str) -> None:
        """Convert between formats.
        
        Args:
            input_file: Input filename
            output_file: Output filename
            output_format: Target format
        """
        data, metadata = FormatHandler.load(input_file)
        FormatHandler.save(data, output_file, output_format, metadata)
        logger.info(f"✓ Converted {input_file} -> {output_file}")
