"""Wireless research utilities: modulation and link budget helpers."""

import math


class WirelessResearch:
    @staticmethod
    def freq_to_wavelength(freq_hz: float) -> float:
        c = 299792458.0
        return c / float(freq_hz)

    @staticmethod
    def free_space_path_loss(freq_hz: float, distance_m: float) -> float:
        # FSPL in dB
        c = 299792458.0
        lam = c / float(freq_hz)
        if distance_m <= 0:
            return float('inf')
        fspl = 20 * math.log10(4 * math.pi * distance_m / lam)
        return fspl
