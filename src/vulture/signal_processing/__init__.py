"""Signal Processing Framework - DSP Algorithms"""
from .filter_bank import FilterBank
from .fir_filter import FIRFilter
from .iir_filter import IIRFilter
from .window_functions import WindowFunctions
from .correlation import CorrelationEngine
from .convolution import ConvolutionEngine
from .synchronization import Synchronizer
from .matched_filter import MatchedFilter

__all__ = [
    'FilterBank', 'FIRFilter', 'IIRFilter', 'WindowFunctions',
    'CorrelationEngine', 'ConvolutionEngine', 'Synchronizer', 'MatchedFilter'
]
