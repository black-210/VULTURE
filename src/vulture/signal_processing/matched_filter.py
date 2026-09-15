"""Matched filter for signal detection."""
import numpy as np
from scipy import signal
import logging
logger = logging.getLogger(__name__)
class MatchedFilter:
    def __init__(self, template):
        self.template = template
        self.filter_coeffs = np.flip(np.conj(template))
    def apply(self, data):
        output = np.convolve(data, self.filter_coeffs, mode='same')
        return output
    def get_detection_threshold(self, data, pfa=1e-4):
        noise_power = np.var(data)
        template_power = np.sum(np.abs(self.template)**2)
        snr_threshold = -2 * np.log(pfa)
        threshold = np.sqrt(snr_threshold * noise_power * template_power)
        return threshold

    def detect_signal(self, data, threshold):
        output = self.apply(data)
        detections = np.where(output > threshold)[0]
        return detections
    def plot_matched_filter_response(self):
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(self.filter_coeffs)
        plt.title("Matched Filter Coefficients")
        plt.xlabel("Sample Index")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.show()
        plt.figure()
        plt.plot(np.abs(self.filter_coeffs))
        plt.title("Matched Filter Magnitude Response")
        plt.xlabel("Sample Index")
        plt.ylabel("Magnitude")
        plt.grid()
        plt.show()