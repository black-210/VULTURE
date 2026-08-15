"""Signal Processing: Filters, windowing, correlation, matched filtering, synchronization, GPU."""

from vulture.signal_processing.filters import Filters
from vulture.signal_processing.windowing import WindowManager
from vulture.signal_processing.correlation import CorrelationEngine
from vulture.signal_processing.matched_filter import MatchedFilter
from vulture.signal_processing.synchronization import Synchronization
from vulture.signal_processing.gpu_acceleration import GPUAcceleration

__all__ = [
    "Filters",
    "WindowManager",
    "CorrelationEngine",
    "MatchedFilter",
    "Synchronization",
    "GPUAcceleration",
]
