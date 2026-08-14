"""IQ data playback."""
import numpy as np
import logging
logger = logging.getLogger(__name__)
class IQPlayback:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.position = 0
    def load(self, format='npy'):
        try:
            if format == 'npy':
                self.data = np.load(self.filename)
            elif format == 'bin':
                self.data = np.fromfile(self.filename, dtype=np.complex64)
            elif format == 'wav':
                import scipy.io.wavfile as wavfile
                _, self.data = wavfile.read(self.filename)
            self.position = 0
            logger.info(f"Loaded {len(self.data)} samples from {self.filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to load: {e}")
            return False
    def read_samples(self, num_samples):
        if self.data is None:
            return np.array([])
        end_pos = min(self.position + num_samples, len(self.data))
        samples = self.data[self.position:end_pos]
        self.position = end_pos
        return samples
    def seek(self, position):
        self.position = min(position, len(self.data) if self.data is not None else 0)
    def get_duration(self, sample_rate):
        return len(self.data) / sample_rate if self.data is not None else 0