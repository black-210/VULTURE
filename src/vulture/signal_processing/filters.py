"""FIR and IIR filter implementations."""
import numpy as np
from scipy import signal
import logging
logger = logging.getLogger(__name__)
class FIRFilter:
    def __init__(self, numtaps, cutoff, filter_type='low'):
        self.numtaps = numtaps
        self.cutoff = cutoff
        self.filter_type = filter_type
        self.coeffs = signal.firwin(numtaps, cutoff, pass_zero=(filter_type=='low'))
    def apply(self, data):
        return signal.lfilter(self.coeffs, 1, data)
    def apply_filtfilt(self, data):
        return signal.filtfilt(self.coeffs, 1, data)
class IIRFilter:
    def __init__(self, order, cutoff, filter_type='low'):
        self.order = order
        self.cutoff = cutoff
        self.b, self.a = signal.butter(order, cutoff, btype=filter_type)
    def apply(self, data):
        return signal.lfilter(self.b, self.a, data)
    def apply_filtfilt(self, data):
        return signal.filtfilt(self.b, self.a, data)