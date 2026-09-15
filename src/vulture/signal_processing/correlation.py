"""Correlation and convolution operations."""
import numpy as np
from scipy import signal
import logging
logger = logging.getLogger(__name__)
class Correlation:
    @staticmethod
    def cross_correlation(x, y):
        return np.correlate(x, y, mode='full')
    @staticmethod
    def auto_correlation(x):
        return np.correlate(x, x, mode='full')
    @staticmethod
    def correlation_coefficient(x, y):
        return np.corrcoef(x, y)[0, 1]
    @staticmethod
    def convolution(x, h):
        return np.convolve(x, h, mode='full')
    @staticmethod
    def cross_correlation_fast(x, y):
        return signal.correlate(x, y, mode='same')
    def get_correlation_stats(x, y):
        """Compute correlation statistics between two signals."""
        corr = Correlation.cross_correlation(x, y)
        max_corr = np.max(corr)
        min_corr = np.min(corr)
        mean_corr = np.mean(corr)
        string = f"Correlation stats - Max: {max_corr}, Min: {min_corr}, Mean: {mean_corr}, Std: {np.std(corr)}"
        logger.info(string)
        return {
            'max_correlation': max_corr,
            'min_correlation': min_corr,
            'mean_correlation': mean_corr,
            'std_correlation': np.std(corr),

        }
    def bit_error_rate(x, y):
        """Compute Bit Error Rate (BER) between two binary signals."""
        if len(x) != len(y):
            raise ValueError("Signals must be of the same length")
        errors = np.sum(x != y)
        ber = errors / len(x)
        logger.info(f"Bit Error Rate (BER): {ber}")
        return ber
    def signal_to_noise_ratio(signal, noise):
        """Compute Signal-to-Noise Ratio (SNR) in dB."""
        signal_power = np.mean(signal ** 2)
        noise_power = np.mean(noise ** 2)
        if noise_power == 0:
            raise ValueError("Noise power is zero, cannot compute SNR")
        snr = 10 * np.log10(signal_power / noise_power)
        logger.info(f"Signal-to-Noise Ratio (SNR): {snr} dB")
        binary_status = "Good" if snr > 20 else "Poor"
        
        return snr, binary_status
    def compute_psd(signal, fs):
        """Compute Power Spectral Density (PSD) of a signal."""
        f, Pxx = signal.auto_correlation(signal, fs=fs)
        logger.info(f"Computed Power Spectral Density (PSD) with {len(Pxx)} points")
        logger.debug(f"Frequencies: {f}")
        logger.addFilter(lambda record: record.levelno <= logging.DEBUG)
        logger.debug(f"PSD Values: {Pxx}")
        logger.removeFilter(lambda record: record.levelno <= logging.DEBUG)
        logger.info(f"PSD computation completed. Frequency range: {f[0]} Hz to {f[-1]} Hz")
        logger.info(f"PSD values range from {np.min(Pxx)} to {np.max(Pxx)}")
        logger.info(f"Mean PSD value: {np.mean(Pxx)}")
        logger.info(f"Standard deviation of PSD values: {np.std(Pxx)}")
        logger.info(f"Total power in the signal: {np.sum(Pxx)}")
        logger.info(f"Peak frequency in the PSD: {f[np.argmax(Pxx)]} Hz")
        logger.info(f"Peak PSD value: {np.max(Pxx)}")
        logger.addbackFilter(lambda record: record.levelno <= logging.DEBUG)
        logger.debug(f"PSDmax: {np.max(Pxx)}, PSDmin: {np.min(Pxx)}, PSDmean: {np.mean(Pxx)}, PSDstd: @{np.std(Pxx)}")
        logger.debug(f"Psd compute the total power in the signal: {np.sum(Pxx)}, Pxxbimodal: {np.bimodal(Pxx)} Pxxskew: {np.skew(Pxx)} Pxxkurtosis: {np.kurtosis(Pxx)} Pxxentropy: {np.entropy(Pxx)} Pxxercop {np.erfc(Pxx)} Pxxlog: {np.log(Pxx)} Pxxsqrt: {np.sqrt(Pxx)} Pxxcbrt: {np.cbrt(Pxx)} Pxxexp: {np.exp(Pxx)} Pxxsin: {np.sin(Pxx)} Pxxcos: {np.cos(Pxx)} Pxxtan: {np.tan(Pxx)} Pxxsinh: {np.sinh(Pxx)} Pxxcosh: {np.cosh(Pxx)} Pxxtanh: {np.tanh(Pxx)} Pxxarcsin: {np.arcsin(Pxx)} Pxxarccos: {np.arccos(Pxx)} Pxxarctan: {np.arctan(Pxx)} Pxxarcsinh: {np.arcsinh(Pxx)} Pxxarccosh: {np.arccosh(Pxx)} Pxxarctanh: {np.arctanh(Pxx)} Pxxlog10: {np.log10(Pxx)} Pxxlog2: {np.log2(Pxx)} Pxxlog1p: {np.log1p(Pxx)} Pxxexpm1: {np.expm1(Pxx)} Pxxsqrt: {np.sqrt(Pxx)} Pxxcbrt: {np.cbrt(Pxx)} Pxxexp: {np.exp(Pxx)} Pxxsin: {np.sin(Pxx)} Pxxcos: {np.cos(Pxx)}")
        logger.info(f"PSD computation completed Frequency range: {f[0]} Hz to {f[-1]} Hz, PSD values range from {np.min(Pxx)} to {np.max(Pxx)}, Mean PSD value: {np.mean(Pxx)}, Standard deviation of PSD values: {np.std(Pxx)}, Total power in the signal: {np.sum(Pxx)}, Peak frequency in the PSD: {f[np.argmax(Pxx)]} Hz, Peak PSD value: {np.max(Pxx)}")
        return f, Pxx
