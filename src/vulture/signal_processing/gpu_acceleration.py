"""GPU acceleration for signal processing."""
import numpy as np
import logging
logger = logging.getLogger(__name__)
class GPUAcceleration:
    def __init__(self, use_gpu=True):
        self.use_gpu = use_gpu
        self.gpu_available = False
        try:
            import cupy as cp
            self.cp = cp
            self.gpu_available = True
            logger.info("GPU acceleration enabled")
        except:
            self.use_gpu = False
            logger.warning("GPU not available, using CPU")
    def fft(self, data):
        if self.gpu_available and self.use_gpu:
            gpu_data = self.cp.asarray(data)
            result = self.cp.fft.fft(gpu_data)
            return self.cp.asnumpy(result)
        return np.fft.fft(data)
    def correlate(self, x, y):
        if self.gpu_available and self.use_gpu:
            gpu_x, gpu_y = self.cp.asarray(x), self.cp.asarray(y)
            result = self.cp.correlate(gpu_x, gpu_y)
            return self.cp.asnumpy(result)
        return np.correlate(x, y)
    def filter(self, b, a, x):
        if self.gpu_available and self.use_gpu:
            gpu_b, gpu_a, gpu_x = self.cp.asarray(b), self.cp.asarray(a), self.cp.asarray(x)
            result = self.cp.convolve(gpu_x, gpu_b) / self.cp.convolve(gpu_x, gpu_a)
            return self.cp.asnumpy(result)
        from scipy import signal
        return signal.lfilter(b, a, x)