"""Burst Detector - Transient Signal Detection"""
import numpy as np
from typing import List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)

class BurstDetector:
    """Detect signal bursts and transients"""
    
    def detect_bursts(self, signal: np.ndarray, threshold: float = None,
                     min_duration: int = 10) -> List[Tuple[int, int]]:
        """Detect bursts in signal
        
        Args:
            signal: Input signal (power or amplitude)
            threshold: Detection threshold
            min_duration: Minimum burst duration in samples
        
        Returns:
            List of (start, end) indices
        """
        if threshold is None:
            threshold = np.mean(np.abs(signal)) + 2 * np.std(np.abs(signal))
        
        above_threshold = np.abs(signal) > threshold
        edges = np.diff(above_threshold.astype(int))
        starts = np.where(edges == 1)[0]
        ends = np.where(edges == -1)[0]
        
        bursts = []
        for start, end in zip(starts, ends):
            if end - start >= min_duration:
                bursts.append((start, end))
        
        return bursts
    def compute_burst_statistics(self, signal: np.ndarray, bursts: List[Tuple[int, int]]) -> List[Dict[str, float]]:
        """Compute statistics for detected bursts
        
        Args:
            signal: Input signal
            bursts: List of (start, end) indices
        """
        stats: List[Dict[str, float]] = []
        for start, end in bursts:
            burst_signal = signal[start:end]
            stat = {
                "start": start,
                "end": end,
                "duration": end - start,
                "max_amplitude": np.max(np.abs(burst_signal)),
                "mean_amplitude": np.mean(np.abs(burst_signal)),
                "std_amplitude": np.std(np.abs(burst_signal))
            }
            stats.append(stat)
        return stats
    def detect_transients(self, signal: np.ndarray, threshold: float = None,
                          min_duration: int = 5) -> List[Tuple[int, int]]:
        """Detect transient events in signal
        
        Args:
            signal: Input signal
            threshold: Detection threshold
            min_duration: Minimum transient duration in samples
        
        Returns:
            List of (start, end) indices
        """
        if threshold is None:
            threshold = np.mean(np.abs(signal)) + 3 * np.std(np.abs(signal))
        
        above_threshold = np.abs(signal) > threshold
        edges = np.diff(above_threshold.astype(int))
        starts = np.where(edges == 1)[0]
        ends = np.where(edges == -1)[0]
        
        transients = []
        for start, end in zip(starts, ends):
            if end - start >= min_duration:
                transients.append((start, end))
