"""Physics Laboratory: frequency/wavelength conversions & link budget helpers.
"""
import math


def freq_to_wavelength(freq_hz: float) -> float:
    c = 299792458.0
    return c / float(freq_hz)


def thermal_noise(bandwidth_hz: float, temp_k: float = 290.0) -> float:
    # k*T*B in watts, return in dBW
    k = 1.38064852e-23
    noise_w = k * temp_k * bandwidth_hz
    return 10 * math.log10(noise_w) if noise_w > 0 else float('-inf')
