from typing import Dict
import math

def free_space_path_loss(freq_hz: float, distance_m: float) -> float:
    """Return FSPL in dB."""
    c = 299792458.0
    wavelength = c / freq_hz
    # FSPL(dB) = 20*log10(4*pi*d / lambda)
    return 20 * math.log10((4 * math.pi * distance_m) / wavelength)

class LinkBudget:
    def __init__(self, tx_power_dbm: float, tx_gain_dbi: float, rx_gain_dbi: float, losses_db: float = 0.0):
        self.tx_power_dbm = tx_power_dbm
        self.tx_gain_dbi = tx_gain_dbi
        self.rx_gain_dbi = rx_gain_dbi
        self.losses_db = losses_db

    def estimate_rx_power_dbm(self, freq_hz: float, distance_m: float) -> float:
        fspl = free_space_path_loss(freq_hz, distance_m)
        return self.tx_power_dbm + self.tx_gain_dbi + self.rx_gain_dbi - fspl - self.losses_db
