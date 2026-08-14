"""IQ data recording."""
import numpy as np
import logging
logger = logging.getLogger(__name__)
class IQRecorder:
    def __init__(self, filename, sample_rate, center_freq):
        self.filename = filename
        self.sample_rate = sample_rate
        self.center_freq = center_freq
        self.data = np.array([], dtype=np.complex64)
        self.metadata = {'sample_rate': sample_rate, 'center_freq': center_freq, 'num_samples': 0}
    def append_samples(self, samples):
        self.data = np.concatenate([self.data, samples])
        self.metadata['num_samples'] = len(self.data)
    def save(self, format='npy'):
        try:
            if format == 'npy':
                np.save(self.filename, self.data)
            elif format == 'bin':
                self.data.astype(np.complex64).tofile(self.filename)
            elif format == 'wav':
                import scipy.io.wavfile as wavfile
                wavfile.write(self.filename, int(self.sample_rate), self.data.astype(np.float32))
            logger.info(f"Saved {len(self.data)} samples to {self.filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save: {e}")
            return False
    def get_stats(self):
        return {'duration': len(self.data) / self.sample_rate, 'num_samples': len(self.data), 'max_power': np.max(np.abs(self.data)**2)}