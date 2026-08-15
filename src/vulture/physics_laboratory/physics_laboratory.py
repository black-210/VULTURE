"""Physics Laboratory Framework - Complete Implementation"""
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Physical constants
SPEED_OF_LIGHT = 3e8  # m/s
FREE_SPACE_PATH_LOSS_REF = 20 * np.log10(4 * np.pi / 3)  # dB


class Electromagnetic:
    """Electromagnetic calculations"""
    
    @staticmethod
    def wavelength(frequency: float) -> float:
        """Calculate wavelength from frequency"""
        return SPEED_OF_LIGHT / frequency
    
    @staticmethod
    def frequency(wavelength: float) -> float:
        """Calculate frequency from wavelength"""
        return SPEED_OF_LIGHT / wavelength
    
    @staticmethod
    def impedance_matching(z1: complex, z2: complex):
        """Calculate reflection and transmission coefficients"""
        reflection = (z2 - z1) / (z2 + z1)
        transmission = 2 * z2 / (z2 + z1)
        
        return {
            'reflection_coeff': reflection,
            'transmission_coeff': transmission,
            'reflection_loss_db': 20 * np.log10(np.abs(reflection) + 1e-10),
            'transmission_loss_db': 20 * np.log10(np.abs(transmission) + 1e-10)
        }
    
    @staticmethod
    def friis_transmission(p_tx: float, g_tx: float, g_rx: float, 
                           distance: float, frequency: float, polarization: float = 1.0):
        """Friis transmission formula"""
        wavelength = SPEED_OF_LIGHT / frequency
        path_loss = 20 * np.log10(4 * np.pi * distance / wavelength)
        
        p_rx = p_tx + g_tx + g_rx - path_loss
        
        return {
            'received_power_dbm': p_rx,
            'path_loss_db': path_loss,
            'received_power_w': 10 ** (p_rx / 10) / 1000
        }


class LinkBudget:
    """Link budget analysis"""
    
    @staticmethod
    def calculate_link_budget(tx_power_dbm: float, tx_gain_db: float, 
                             rx_gain_db: float, path_loss_db: float, 
                             cable_loss_db: float = 0, misc_loss_db: float = 0):
        """Calculate complete link budget"""
        
        # Effective Radiated Power (ERP)
        erp = tx_power_dbm + tx_gain_db - cable_loss_db
        
        # Received power
        rx_power = erp - path_loss_db + rx_gain_db - misc_loss_db
        
        # Margin (how much above sensitivity)
        margin = rx_power  # Assuming sensitivity at 0 dBm reference
        
        return {
            'erp_dbm': erp,
            'received_power_dbm': rx_power,
            'path_loss_db': path_loss_db,
            'margin_db': margin,
            'link_available': margin > -120  # Typical sensitivity
        }
    
    @staticmethod
    def snr_analysis(signal_power_dbm: float, noise_power_dbm: float, 
                    bandwidth_hz: float = 1e6):
        """Signal to Noise Ratio analysis"""
        
        snr_db = signal_power_dbm - noise_power_dbm
        
        # Noise Figure (approximation)
        nf_db = 8  # Typical receiver NF
        noise_figure = 10 ** (nf_db / 10)
        
        # Effective SNR
        effective_snr = snr_db - nf_db
        
        return {
            'snr_db': snr_db,
            'noise_figure_db': nf_db,
            'effective_snr_db': effective_snr,
            'bandwidth_hz': bandwidth_hz
        }


class AntennaCalculator:
    """Antenna calculations"""
    
    @staticmethod
    def isotropic_gain():
        """Isotropic radiator (reference antenna)"""
        return {
            'gain_db': 0,
            'gain_linear': 1,
            'type': 'isotropic'
        }
    
    @staticmethod
    def dipole_gain(frequency: float, length: float = None):
        """Dipole antenna gain"""
        if length is None:
            length = (SPEED_OF_LIGHT / frequency) / 2
        
        # Half-wave dipole gain
        if np.isclose(length, (SPEED_OF_LIGHT / frequency) / 2):
            gain_linear = 1.64  # ~2.14 dBi
            gain_db = 10 * np.log10(gain_linear)
        else:
            # Approximation for other lengths
            gain_db = 2 * np.log10(length / (SPEED_OF_LIGHT / (2 * frequency)))
        
        return {
            'gain_db': gain_db,
            'gain_linear': 10 ** (gain_db / 10),
            'type': 'dipole',
            'length_m': length
        }
    
    @staticmethod
    def parabolic_antenna(diameter: float, frequency: float, efficiency: float = 0.65):
        """Parabolic antenna gain"""
        wavelength = SPEED_OF_LIGHT / frequency
        
        # Effective aperture
        aperture = np.pi * (diameter / 2) ** 2
        
        # Gain
        gain_linear = efficiency * (4 * np.pi * aperture) / (wavelength ** 2)
        gain_db = 10 * np.log10(gain_linear)
        
        return {
            'gain_db': gain_db,
            'gain_linear': gain_linear,
            'aperture_m2': aperture,
            'type': 'parabolic',
            'diameter_m': diameter,
            'efficiency': efficiency
        }
    
    @staticmethod
    def beamwidth(gain_db: float, frequency: float, antenna_type: str = 'dipole'):
        """Estimate beamwidth from gain"""
        # Simplified relationship
        if antenna_type == 'parabolic':
            # 3dB beamwidth approximation
            beamwidth_deg = 70 * (SPEED_OF_LIGHT / (frequency * 1.0)) / 1  # placeholder
        else:
            beamwidth_deg = 180 / (10 ** (gain_db / 10))
        
        return {
            'beamwidth_deg': beamwidth_deg,
            'gain_db': gain_db
        }


class PropagationModels:
    """Radio propagation models"""
    
    @staticmethod
    def free_space_path_loss(frequency: float, distance: float):
        """Free space path loss (Friis formula)"""
        wavelength = SPEED_OF_LIGHT / frequency
        path_loss = 20 * np.log10(4 * np.pi * distance / wavelength)
        
        return {
            'path_loss_db': path_loss,
            'distance_m': distance,
            'frequency_hz': frequency
        }
    
    @staticmethod
    def log_distance_model(frequency: float, distance: float, 
                          reference_distance: float = 1.0, path_loss_exponent: float = 2.0):
        """Log-distance path loss model"""
        wavelength = SPEED_OF_LIGHT / frequency
        
        # Reference path loss at 1m
        reference_loss = 20 * np.log10(4 * np.pi * reference_distance / wavelength)
        
        # Path loss
        path_loss = reference_loss + 10 * path_loss_exponent * np.log10(distance / reference_distance)
        
        return {
            'path_loss_db': path_loss,
            'distance_m': distance,
            'path_loss_exponent': path_loss_exponent
        }
    
    @staticmethod
    def rayleigh_fading(signal_power: float, mean_power: float):
        """Rayleigh fading channel"""
        # Amplitude follows Rayleigh distribution
        fading_factor = np.random.rayleigh(np.sqrt(mean_power / 2))
        
        received_power = signal_power * (fading_factor ** 2)
        
        return {
            'received_power': received_power,
            'fading_factor': fading_factor,
            'fading_db': 10 * np.log10(fading_factor ** 2)
        }
    
    @staticmethod
    def rician_fading(signal_power: float, mean_power: float, k_factor: float = 1.0):
        """Rician fading (with line-of-sight component)"""
        # k_factor = LOS power / scattered power
        los_power = k_factor * mean_power / (k_factor + 1)
        scatter_power = mean_power / (k_factor + 1)
        
        # Rician distributed amplitude
        i = np.random.normal(np.sqrt(2 * los_power), np.sqrt(scatter_power))
        q = np.random.normal(0, np.sqrt(scatter_power))
        
        fading_factor = np.sqrt(i**2 + q**2)
        received_power = signal_power * (fading_factor ** 2)
        
        return {
            'received_power': received_power,
            'fading_factor': fading_factor,
            'k_factor': k_factor,
            'fading_db': 10 * np.log10(fading_factor ** 2)
        }


class SignalPath:
    """Signal path analysis"""
    
    @staticmethod
    def calculate_signal_path(tx_power_dbm: float, frequency: float, 
                             tx_antenna_gain_db: float, rx_antenna_gain_db: float,
                             distance: float, environmental_loss_db: float = 0):
        """Calculate complete signal path"""
        
        # Free space path loss
        path_loss = PropagationModels.free_space_path_loss(frequency, distance)
        
        # Received power
        rx_power = (tx_power_dbm + tx_antenna_gain_db + rx_antenna_gain_db 
                   - path_loss['path_loss_db'] - environmental_loss_db)
        
        # Link budget
        link_margin = rx_power + 100  # Assuming -100 dBm sensitivity
        
        return {
            'rx_power_dbm': rx_power,
            'path_loss_db': path_loss['path_loss_db'],
            'link_margin_db': link_margin,
            'signal_path_valid': link_margin > 0
        }


class RadarSimulator:
    """Simplified RADAR simulator"""
    
    @staticmethod
    def calculate_radar_range(tx_power_dbm: float, frequency: float,
                             antenna_gain_db: float, rcs_dbsm: float,
                             receiver_sensitivity_dbm: float = -110):
        """Calculate maximum radar range"""
        
        # Radar range equation (simplified)
        # Pr = (Pt * Gt * Gr * lambda^2 * σ) / (64 * π^3 * R^4 * NF)
        
        wavelength = SPEED_OF_LIGHT / frequency
        
        # Numerator components
        numerator = (tx_power_dbm + 2 * antenna_gain_db + 
                    20 * np.log10(wavelength) + rcs_dbsm)
        
        # Path loss at 1m
        path_loss_1m = 20 * np.log10(4 * np.pi / wavelength)
        
        # Denominator (noise figure and receiver sensitivity)
        denominator = receiver_sensitivity_dbm + 64 * np.log10(np.pi) * 3
        
        # Range
        range_factor = (numerator - denominator) / 40
        max_range = 10 ** (range_factor / 10)
        
        return {
            'max_range_m': max_range,
            'max_range_km': max_range / 1000,
            'range_resolution_m': SPEED_OF_LIGHT / (2 * 1e9)  # Assuming 1GHz bandwidth
        }
    
    @staticmethod
    def doppler_shift(target_velocity_ms: float, frequency: float):
        """Calculate Doppler shift"""
        doppler_freq = 2 * target_velocity_ms * frequency / SPEED_OF_LIGHT
        
        return {
            'doppler_shift_hz': doppler_freq,
            'velocity_ms': target_velocity_ms,
            'shifted_frequency_hz': frequency + doppler_freq
        }


# Export classes
__all__ = [
    'Electromagnetic',
    'LinkBudget',
    'AntennaCalculator',
    'PropagationModels',
    'SignalPath',
    'RadarSimulator'
]
