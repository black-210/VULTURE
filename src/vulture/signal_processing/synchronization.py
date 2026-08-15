"""Symbol timing recovery and carrier recovery PLL."""

import numpy as np
from scipy import signal
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class Synchronization:
    """Symbol and carrier synchronization."""

    @staticmethod
    def gardner_timing_recovery(data: np.ndarray, samples_per_symbol: int,
                               mu: float = 0.01) -> Tuple[np.ndarray, float]:
        """Gardner timing error detector.
        
        Args:
            data: Input signal
            samples_per_symbol: Oversampling factor
            mu: Adaptation constant
            
        Returns:
            (recovered_symbols, estimated_offset)
        """
        symbols = []
        tau = 0
        
        for i in range(samples_per_symbol, len(data) - samples_per_symbol):
            # Gardner error detector
            idx_early = int(i - samples_per_symbol/2 + tau)
            idx_on_time = int(i + tau)
            idx_late = int(i + samples_per_symbol/2 + tau)
            
            if idx_early >= 0 and idx_late < len(data):
                early = data[idx_early]
                on_time = data[idx_on_time]
                late = data[idx_late]
                
                error = (early - late) * np.conj(on_time)
                tau += mu * np.imag(error)
                symbols.append(on_time)
        
        return np.array(symbols), tau

    @staticmethod
    def costas_pll(data: np.ndarray, alpha: float = 0.01, 
                   beta: float = 0.001) -> Tuple[np.ndarray, np.ndarray]:
        """Costas Phase-Locked Loop for carrier recovery.
        
        Args:
            data: Input signal
            alpha: Loop filter coefficient 1
            beta: Loop filter coefficient 2
            
        Returns:
            (recovered_signal, estimated_phase)
        """
        output = []
        phase = 0
        freq_offset = 0
        
        for sample in data:
            # Mix with estimated carrier
            mixed = sample * np.exp(-1j * phase)
            
            # Loop filter (simplified)
            error = np.imag(mixed) * np.sign(np.real(mixed))
            freq_offset += beta * error
            phase += freq_offset + alpha * error
            
            phase = np.mod(phase, 2 * np.pi)
            output.append(mixed)
        
        return np.array(output), np.array([np.angle(s) for s in output])
