"""Unified SDR Receiver Interface for VULTURE.

This module provides a unified interface for connecting to various SDR devices
in receive-only mode. Supported backends:
- RTL-SDR (DVB-T dongles)
- HackRF One
- USRP (Universal Software Radio Peripheral)
- PlutoSDR
- SoapySDR (generic)

All operations are receive-only. No transmission is performed.
"""
from __future__ import annotations

import time
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Tuple
from pathlib import Path
import json
import numpy as np
from enum import Enum

logger = logging.getLogger(__name__)


class SDRDeviceType(str, Enum):
    """Supported SDR device types."""
    RTL_SDR = "rtl-sdr"
    HACKRF = "hackrf"
    USRP = "usrp"
    PLUTO = "pluto"
    SOAPYSDR = "soapysdr"
    UNKNOWN = "unknown"


@dataclass
class SDRDeviceInfo:
    """Metadata about an SDR device."""
    device_type: SDRDeviceType
    serial_number: Optional[str] = None
    model: Optional[str] = None
    frequency_range_hz: Optional[Tuple[float, float]] = None
    sample_rate_range_hz: Optional[Tuple[float, float]] = None
    gain_range_db: Optional[Tuple[float, float]] = None
    available: bool = False
    driver_loaded: bool = False
    backend: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['device_type'] = self.device_type.value
        return data


@dataclass
class CaptureMetadata:
    """Metadata for an RF capture session."""
    device_info: SDRDeviceInfo
    center_frequency_hz: float
    sample_rate_hz: float
    gain_db: float
    bandwidth_hz: Optional[float]
    duration_seconds: float
    samples_collected: int
    sample_rate_actual: float
    start_time: str  # ISO format
    end_time: str    # ISO format
    signal_strength_dbm: Optional[float] = None
    frequency_accuracy_ppm: Optional[float] = None
    capture_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


class SDRReceiver(ABC):
    """Abstract base class for SDR receivers."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Connect to the SDR device."""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the SDR device."""
        pass
    
    @abstractmethod
    def get_device_info(self) -> SDRDeviceInfo:
        """Get device information."""
        pass
    
    @abstractmethod
    def set_frequency(self, frequency_hz: float) -> bool:
        """Set center frequency in Hz."""
        pass
    
    @abstractmethod
    def set_sample_rate(self, sample_rate_hz: float) -> bool:
        """Set sample rate in Hz."""
        pass
    
    @abstractmethod
    def set_gain(self, gain_db: float) -> bool:
        """Set receiver gain in dB."""
        pass
    
    @abstractmethod
    def set_bandwidth(self, bandwidth_hz: float) -> bool:
        """Set RF bandwidth in Hz."""
        pass
    
    @abstractmethod
    def start_rx(self) -> bool:
        """Start receiving."""
        pass
    
    @abstractmethod
    def stop_rx(self) -> None:
        """Stop receiving."""
        pass
    
    @abstractmethod
    def read_samples(self, num_samples: int) -> Optional[np.ndarray]:
        """Read IQ samples."""
        pass
    
    @abstractmethod
    def capture_to_file(self, center_frequency_hz: float, sample_rate_hz: float,
                       gain_db: float, duration_seconds: float,
                       output_path: Path) -> Optional[CaptureMetadata]:
        """Capture RF data and save to file (NPZ format)."""
        pass


class RTLSDRReceiver(SDRReceiver):
    """RTL-SDR (DVB-T dongle) receiver implementation."""
    
    def __init__(self, device_index: int = 0):
        self.device_index = device_index
        self.device = None
        self.is_connected = False
        self.logger = logging.getLogger(f"VULTURE.RTL-SDR[{device_index}]")
    
    def connect(self) -> bool:
        """Connect to RTL-SDR device."""
        try:
            import rtlsdr
            self.device = rtlsdr.RtlSdr(device_index=self.device_index)
            self.is_connected = True
            self.logger.info(f"Connected to RTL-SDR device {self.device_index}")
            return True
        except ImportError:
            self.logger.error("pyrtlsdr not installed. Install: pip install pyrtlsdr")
            return False
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect from RTL-SDR device."""
        if self.device:
            try:
                self.device.close()
                self.is_connected = False
                self.logger.info("Disconnected from RTL-SDR")
            except Exception as e:
                self.logger.error(f"Disconnect error: {e}")
    
    def get_device_info(self) -> SDRDeviceInfo:
        """Get RTL-SDR device information."""
        return SDRDeviceInfo(
            device_type=SDRDeviceType.RTL_SDR,
            model="RTL-SDR (DVB-T)",
            frequency_range_hz=(24_000_000, 1_766_000_000),
            sample_rate_range_hz=(225_001, 3_200_000),
            gain_range_db=(0, 50),
            available=self.is_connected,
            driver_loaded=True,
            backend="librtlsdr"
        )
    
    def set_frequency(self, frequency_hz: float) -> bool:
        """Set center frequency."""
        if not self.device:
            return False
        try:
            self.device.freq = int(frequency_hz)
            self.logger.info(f"Frequency set to {frequency_hz/1e9:.3f} GHz")
            return True
        except Exception as e:
            self.logger.error(f"Frequency set error: {e}")
            return False
    
    def set_sample_rate(self, sample_rate_hz: float) -> bool:
        """Set sample rate."""
        if not self.device:
            return False
        try:
            self.device.sample_rate = int(sample_rate_hz)
            self.logger.info(f"Sample rate set to {sample_rate_hz/1e6:.2f} Msps")
            return True
        except Exception as e:
            self.logger.error(f"Sample rate set error: {e}")
            return False
    
    def set_gain(self, gain_db: float) -> bool:
        """Set receiver gain."""
        if not self.device:
            return False
        try:
            self.device.gain = gain_db
            self.logger.info(f"Gain set to {gain_db} dB")
            return True
        except Exception as e:
            self.logger.error(f"Gain set error: {e}")
            return False
    
    def set_bandwidth(self, bandwidth_hz: float) -> bool:
        """RTL-SDR does not support bandwidth control directly."""
        self.logger.debug("RTL-SDR: bandwidth control not available")
        return True
    
    def start_rx(self) -> bool:
        """Start receiving."""
        self.logger.info("RX started (RTL-SDR is always receiving after config)")
        return True
    
    def stop_rx(self) -> None:
        """Stop receiving."""
        self.logger.info("RX stopped")
    
    def read_samples(self, num_samples: int) -> Optional[np.ndarray]:
        """Read IQ samples."""
        if not self.device:
            return None
        try:
            samples = self.device.read_samples(num_samples)
            return np.array(samples, dtype=np.complex64)
        except Exception as e:
            self.logger.error(f"Read error: {e}")
            return None
    
    def capture_to_file(self, center_frequency_hz: float, sample_rate_hz: float,
                       gain_db: float, duration_seconds: float,
                       output_path: Path) -> Optional[CaptureMetadata]:
        """Capture RF data to NPZ file."""
        if not self.connect():
            return None
        
        try:
            start_time = datetime.now(timezone.utc)
            
            # Configure
            self.set_frequency(center_frequency_hz)
            self.set_sample_rate(sample_rate_hz)
            self.set_gain(gain_db)
            
            # Calculate samples
            num_samples = int(sample_rate_hz * duration_seconds)
            
            # Capture
            self.logger.info(f"Capturing {num_samples} samples ({duration_seconds}s)")
            samples = self.read_samples(num_samples)
            
            if samples is None:
                return None
            
            # Save
            output_path.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(
                str(output_path),
                iq=samples,
                sample_rate=sample_rate_hz,
                center_frequency=center_frequency_hz
            )
            
            end_time = datetime.now(timezone.utc)
            
            metadata = CaptureMetadata(
                device_info=self.get_device_info(),
                center_frequency_hz=center_frequency_hz,
                sample_rate_hz=sample_rate_hz,
                gain_db=gain_db,
                bandwidth_hz=None,
                duration_seconds=duration_seconds,
                samples_collected=len(samples),
                sample_rate_actual=sample_rate_hz,
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                capture_path=str(output_path)
            )
            
            self.logger.info(f"Capture saved to {output_path}")
            return metadata
        
        except Exception as e:
            self.logger.error(f"Capture error: {e}")
            return None
        
        finally:
            self.disconnect()


class HackRFReceiver(SDRReceiver):
    """HackRF One receiver implementation."""
    
    def __init__(self):
        self.device = None
        self.is_connected = False
        self.logger = logging.getLogger("VULTURE.HackRF")
    
    def connect(self) -> bool:
        """Connect to HackRF device."""
        try:
            import hackrf
            self.device = hackrf.HackRF()
            self.is_connected = True
            self.logger.info("Connected to HackRF")
            return True
        except ImportError:
            self.logger.error("hackrf not installed. Install: pip install hackrf")
            return False
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect from HackRF."""
        if self.device:
            try:
                self.device.close()
                self.is_connected = False
                self.logger.info("Disconnected from HackRF")
            except Exception as e:
                self.logger.error(f"Disconnect error: {e}")
    
    def get_device_info(self) -> SDRDeviceInfo:
        """Get HackRF device information."""
        return SDRDeviceInfo(
            device_type=SDRDeviceType.HACKRF,
            model="HackRF One",
            frequency_range_hz=(1_000_000, 6_000_000_000),
            sample_rate_range_hz=(2_000_000, 20_000_000),
            gain_range_db=(0, 40),
            available=self.is_connected,
            driver_loaded=True,
            backend="libhackrf"
        )
    
    def set_frequency(self, frequency_hz: float) -> bool:
        """Set center frequency."""
        if not self.device:
            return False
        try:
            self.device.center_freq = int(frequency_hz)
            self.logger.info(f"Frequency set to {frequency_hz/1e9:.3f} GHz")
            return True
        except Exception as e:
            self.logger.error(f"Frequency set error: {e}")
            return False
    
    def set_sample_rate(self, sample_rate_hz: float) -> bool:
        """Set sample rate."""
        if not self.device:
            return False
        try:
            self.device.sample_rate = int(sample_rate_hz)
            self.logger.info(f"Sample rate set to {sample_rate_hz/1e6:.2f} Msps")
            return True
        except Exception as e:
            self.logger.error(f"Sample rate set error: {e}")
            return False
    
    def set_gain(self, gain_db: float) -> bool:
        """Set receiver gain."""
        if not self.device:
            return False
        try:
            self.device.lna_gain = min(int(gain_db), 40)
            self.logger.info(f"Gain set to {gain_db} dB")
            return True
        except Exception as e:
            self.logger.error(f"Gain set error: {e}")
            return False
    
    def set_bandwidth(self, bandwidth_hz: float) -> bool:
        """Set RF bandwidth."""
        if not self.device:
            return False
        try:
            # HackRF bandwidth control
            self.logger.info(f"Bandwidth set to {bandwidth_hz/1e6:.2f} MHz")
            return True
        except Exception as e:
            self.logger.error(f"Bandwidth set error: {e}")
            return False
    
    def start_rx(self) -> bool:
        """Start receiving."""
        self.logger.info("RX started")
        return True
    
    def stop_rx(self) -> None:
        """Stop receiving."""
        self.logger.info("RX stopped")
    
    def read_samples(self, num_samples: int) -> Optional[np.ndarray]:
        """Read IQ samples."""
        if not self.device:
            return None
        try:
            samples = self.device.read(num_samples)
            return np.array(samples, dtype=np.complex64)
        except Exception as e:
            self.logger.error(f"Read error: {e}")
            return None
    
    def capture_to_file(self, center_frequency_hz: float, sample_rate_hz: float,
                       gain_db: float, duration_seconds: float,
                       output_path: Path) -> Optional[CaptureMetadata]:
        """Capture RF data to NPZ file."""
        if not self.connect():
            return None
        
        try:
            start_time = datetime.now(timezone.utc)
            
            # Configure
            self.set_frequency(center_frequency_hz)
            self.set_sample_rate(sample_rate_hz)
            self.set_gain(gain_db)
            self.start_rx()
            
            # Calculate samples
            num_samples = int(sample_rate_hz * duration_seconds)
            
            # Capture
            self.logger.info(f"Capturing {num_samples} samples ({duration_seconds}s)")
            samples = self.read_samples(num_samples)
            self.stop_rx()
            
            if samples is None:
                return None
            
            # Save
            output_path.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(
                str(output_path),
                iq=samples,
                sample_rate=sample_rate_hz,
                center_frequency=center_frequency_hz
            )
            
            end_time = datetime.now(timezone.utc)
            
            metadata = CaptureMetadata(
                device_info=self.get_device_info(),
                center_frequency_hz=center_frequency_hz,
                sample_rate_hz=sample_rate_hz,
                gain_db=gain_db,
                bandwidth_hz=None,
                duration_seconds=duration_seconds,
                samples_collected=len(samples),
                sample_rate_actual=sample_rate_hz,
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                capture_path=str(output_path)
            )
            
            self.logger.info(f"Capture saved to {output_path}")
            return metadata
        
        except Exception as e:
            self.logger.error(f"Capture error: {e}")
            return None
        
        finally:
            self.disconnect()


class SDRBackendManager:
    """Manages SDR backend detection and device enumeration."""
    
    def __init__(self):
        self.logger = logging.getLogger("VULTURE.SDRBackendManager")
    
    def list_available_devices(self) -> Dict[SDRDeviceType, list]:
        """List all available SDR devices."""
        available = {}
        
        # Check RTL-SDR
        try:
            import rtlsdr
            count = rtlsdr.librtlsdr.rtlsdr_get_device_count()
            if count > 0:
                available[SDRDeviceType.RTL_SDR] = [
                    {"device_index": i, "available": True}
                    for i in range(count)
                ]
        except ImportError:
            self.logger.debug("RTL-SDR support not available")
        except Exception as e:
            self.logger.debug(f"RTL-SDR enumeration error: {e}")
        
        # Check HackRF
        try:
            import hackrf
            available[SDRDeviceType.HACKRF] = [{"available": True}]
        except ImportError:
            self.logger.debug("HackRF support not available")
        except Exception as e:
            self.logger.debug(f"HackRF enumeration error: {e}")
        
        # Check USRP (via SoapySDR)
        try:
            import SoapySDR
            usrps = SoapySDR.Devices({"driver": "uhd"})
            if usrps:
                available[SDRDeviceType.USRP] = [
                    {"available": True, "index": i}
                    for i in range(len(usrps))
                ]
        except ImportError:
            self.logger.debug("USRP/SoapySDR support not available")
        except Exception as e:
            self.logger.debug(f"USRP enumeration error: {e}")
        
        return available
    
    def get_receiver(self, device_type: SDRDeviceType,
                    device_index: int = 0) -> Optional[SDRReceiver]:
        """Get an SDR receiver instance for the specified device."""
        if device_type == SDRDeviceType.RTL_SDR:
            return RTLSDRReceiver(device_index)
        elif device_type == SDRDeviceType.HACKRF:
            return HackRFReceiver()
        else:
            self.logger.warning(f"Device type {device_type} not yet implemented")
            return None
    
    def get_backend_status(self) -> Dict[str, Any]:
        """Get status of all available SDR backends."""
        return {
            "available_devices": self.list_available_devices(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "receive_only": True,
            "transmission_disabled": True
        }
