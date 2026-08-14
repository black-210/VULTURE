"""Format handler for various IQ data formats."""
import numpy as np
import logging
logger = logging.getLogger(__name__)
class FormatHandler:
    @staticmethod
    def convert_format(input_file, output_file, input_fmt, output_fmt):
        data = None
        if input_fmt == 'npy':
            data = np.load(input_file)
        elif input_fmt == 'bin':
            data = np.fromfile(input_file, dtype=np.complex64)
        elif input_fmt == 'csv':
            data = np.loadtxt(input_file, dtype=complex, delimiter=',')
        if data is None:
            return False
        if output_fmt == 'npy':
            np.save(output_file, data)
        elif output_fmt == 'bin':
            data.astype(np.complex64).tofile(output_file)
        elif output_fmt == 'csv':
            np.savetxt(output_file, data, fmt='%s', delimiter=',')
        logger.info(f"Converted {input_fmt} to {output_fmt}")
        return True
    @staticmethod
    def detect_format(filename):
        ext = filename.split('.')[-1].lower()
        if ext == 'npy':
            return 'npy'
        elif ext == 'bin':
            return 'bin'
        elif ext == 'wav':
            return 'wav'
        elif ext == 'csv':
            return 'csv'
        return 'unknown'
    @staticmethod
    def get_format_info(filename, format_type):
        try:
            if format_type == 'npy':
                data = np.load(filename)
            elif format_type == 'bin':
                data = np.fromfile(filename, dtype=np.complex64)
            else:
                return {}
            return {'shape': data.shape, 'dtype': str(data.dtype), 'size_mb': data.nbytes / 1e6}
        except Exception as e:
            logger.error(f"Error getting format info: {e}")
            return {}