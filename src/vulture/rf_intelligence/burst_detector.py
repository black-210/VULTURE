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
