"""
SDR / IQ framework package stubs.
Hardware Abstraction, IQ IO, format detection, metadata extraction.
"""
from .hardware import HardwareInterface
from .iqio import IQRecorder, IQPlayer
from .format import detect_format
from .metadata import extract_metadata

__all__ = ["HardwareInterface", "IQRecorder", "IQPlayer", "detect_format", "extract_metadata"]
