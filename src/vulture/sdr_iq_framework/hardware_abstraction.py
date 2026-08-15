"""Hardware abstraction: RTL-SDR, UHD, PlutoSDR."""

import numpy as np
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class HardwareAbstraction:
    """Unified interface for RF hardware."""

    def __init__(self, hw_type: str = 'rtlsdr'):
        """
        Args:
            hw_type: 'rtlsdr', 'uhd', 'pluto'
        """
        self.hw_type = hw_type
        self.device = None
        self.sample_rate = 2e6
        self.center_freq = 1e9
        self.gain = 20
        self.is_open = False

    def open_device(self, device_id: int = 0) -> None:
        """Open hardware device.
        
        Args:
            device_id: Device index
        """
        try:
            if self.hw_type == 'rtlsdr':
                import rtlsdr
                self.device = rtlsdr.RtlSdr(device_id)
                logger.info(f"✓ RTL-SDR device opened: {self.device.serial}")
            elif self.hw_type == 'uhd':
                import uhd
                self.device = uhd.usrp.MultiUsrp(f"serial=" if device_id == 0 else f"addr0=127.0.0.1")
                logger.info("✓ UHD device opened")
            elif self.hw_type == 'pluto':
                import adi
                self.device = adi.Pluto(f"ip:{['192.168.2.1', 'ip:localhost'][device_id]}")
                logger.info("✓ PlutoSDR device opened")
            self.is_open = True
        except Exception as e:
            logger.error(f"✗ Failed to open {self.hw_type}: {e}")
            raise

    def close_device(self) -> None:
        """Close device."""
        if self.device and self.is_open:
            try:
                self.device.close()
                self.is_open = False
                logger.info("✓ Device closed")
            except Exception as e:
                logger.error(f"✗ Error closing device: {e}")

    def set_center_freq(self, freq: float) -> None:
        """Set center frequency.
        
        Args:
            freq: Frequency in Hz
        """
        if not self.is_open:
            raise RuntimeError("Device not open")
        try:
            self.device.center_freq = freq
            self.center_freq = freq
            logger.debug(f"Center freq set to {freq/1e9:.2f} GHz")
        except Exception as e:
            logger.error(f"✗ Set freq failed: {e}")

    def set_sample_rate(self, rate: float) -> None:
        """Set sample rate.
        
        Args:
            rate: Sample rate in Hz
        """
        if not self.is_open:
            raise RuntimeError("Device not open")
        try:
            self.device.sample_rate = rate
            self.sample_rate = rate
            logger.debug(f"Sample rate set to {rate/1e6:.2f} MHz")
        except Exception as e:
            logger.error(f"✗ Set sample rate failed: {e}")

    def set_gain(self, gain: float | str = 'auto') -> None:
        """Set gain.
        
        Args:
            gain: Gain value or 'auto'
        """
        if not self.is_open:
            raise RuntimeError("Device not open")
        try:
            if gain == 'auto':
                self.device.gain = 'auto'
            else:
                self.device.gain = gain
            self.gain = gain
            logger.debug(f"Gain set to {gain}")
        except Exception as e:
            logger.error(f"✗ Set gain failed: {e}")

    def read_samples(self, num_samples: int) -> np.ndarray:
        """Read samples from device.
        
        Args:
            num_samples: Number of samples
            
        Returns:
            Complex IQ samples
        """
        if not self.is_open:
            raise RuntimeError("Device not open")
        try:
            samples = self.device.read_samples(num_samples)
            return np.array(samples, dtype=np.complex64)
        except Exception as e:
            logger.error(f"✗ Read failed: {e}")
            raise
