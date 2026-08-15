from typing import Dict

class Antenna:
    """Simple antenna helper calculations (gain, effective area, beamwidth)."""

    def __init__(self, gain_dbi: float = 0.0, frequency_hz: float = 1e9) -> None:
        self.gain_dbi = gain_dbi
        self.frequency_hz = frequency_hz

    def effective_area(self) -> float:
        """Calculate effective aperture (A_e) from gain and frequency.
        A_e = (G * lambda^2) / (4*pi)
        """
        import math
        c = 299792458.0
        wavelength = c / self.frequency_hz
        g_linear = 10 ** (self.gain_dbi / 10.0)
        return (g_linear * wavelength ** 2) / (4 * math.pi)
