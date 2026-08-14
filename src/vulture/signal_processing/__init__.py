"""Signal Processing Framework - Filters, windowing, and DSP operations."""
from .filters import FIRFilter, IIRFilter
from .windowing import WindowingFunctions
from .correlation import Correlation
from .matched_filter import MatchedFilter
from .synchronization import Synchronization
from .gpu_acceleration import GPUAcceleration
__all__ = ['FIRFilter', 'IIRFilter', 'WindowingFunctions', 'Correlation', 'MatchedFilter', 'Synchronization', 'GPUAcceleration']