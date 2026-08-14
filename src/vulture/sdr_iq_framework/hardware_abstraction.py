"""Hardware abstraction layer for SDR devices."""
import numpy as np
import logging
logger = logging.getLogger(__name__)
class HardwareAbstraction:
    def __init__(self, device_type='rtlsdr'):
        self.device_type = device_type
        self.device = None
        self.is_open = False
    def open_device(self, device_id=0):
        try:
            if self.device_type == 'rtlsdr':
                import rtlsdr
                self.device = rtlsdr.RtlSdr(device_id)
            elif self.device_type == 'uhd':
                import uhd
                self.device = uhd.usrp.MultiUSRP()
            elif self.device_type == 'pluto':
                import adi
                self.device = adi.Pluto()
            self.is_open = True
            logger.info(f"Opened {self.device_type} device {device_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to open device: {e}")
            return False
    def close_device(self):
        if self.device and self.is_open:
            self.device.close()
            self.is_open = False
            logger.info("Device closed")
    def set_center_freq(self, freq):
        if self.device:
            self.device.center_freq = freq
    def set_sample_rate(self, rate):
        if self.device:
            self.device.sample_rate = rate
    def set_gain(self, gain):
        if self.device:
            self.device.gain = gain
    def read_samples(self, num_samples):
        if self.device:
            return self.device.read_samples(num_samples)
        return np.array([])
    def get_device_info(self):
        info = {'device_type': self.device_type, 'is_open': self.is_open}
        if self.device:
            info['center_freq'] = self.device.center_freq
            info['sample_rate'] = self.device.sample_rate
            info['gain'] = self.device.gain
        return info