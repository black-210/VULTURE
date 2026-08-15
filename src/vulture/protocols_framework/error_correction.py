"""Error correction and coding."""

import numpy as np
import logging

logger = logging.getLogger(__name__)

class ErrorCorrection:
    """Error correction coding techniques."""
    
    @staticmethod
    def hamming_encode(data, parity_bits=4):
        """Hamming code encoding."""
        data_bits = len(data)
        total_bits = data_bits + parity_bits
        encoded = [0] * total_bits
        
        # Place data bits
        data_idx = 0
        for i in range(1, total_bits):
            if (i & (i-1)) != 0:  # Not a power of 2
                if data_idx < data_bits:
                    encoded[i-1] = data[data_idx]
                    data_idx += 1
        
        # Calculate parity bits
        for i in range(parity_bits):
            parity_pos = 2**i - 1
            parity = 0
            for j in range(total_bits):
                if (j+1) & (2**i):
                    parity ^= encoded[j]
            encoded[parity_pos] = parity
        
        return np.array(encoded)
    
    @staticmethod
    def hamming_decode(encoded, parity_bits=4):
        """Hamming code decoding with error correction."""
        total_bits = len(encoded)
        error_pos = 0
        
        # Calculate syndrome
        for i in range(parity_bits):
            parity = 0
            for j in range(total_bits):
                if (j+1) & (2**i):
                    parity ^= encoded[j]
            if parity:
                error_pos += 2**i
        
        # Correct error if found
        if error_pos > 0:
            encoded = encoded.copy()
            encoded[error_pos-1] ^= 1
        
        # Extract data
        data = []
        for i in range(1, total_bits):
            if (i & (i-1)) != 0:  # Not a power of 2
                data.append(encoded[i-1])
        
        return np.array(data)
    
    @staticmethod
    def convolutional_encode(data, generator=[7, 5]):
        """Simple convolutional encoding."""
        encoded = []
        shift_register = 0
        
        for bit in data:
            shift_register = ((shift_register << 1) | bit) & 0x7
            
            output = 0
            for i, gen in enumerate(generator):
                parity = bin(shift_register & gen).count('1') % 2
                output = (output << 1) | parity
            
            encoded.append(output)
        
        return np.array(encoded)
    
    @staticmethod
    def crc_checksum(data, polynomial=0x1021):
        """CRC checksum calculation."""
        crc = 0xFFFF
        
        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                crc <<= 1
                if crc & 0x10000:
                    crc ^= polynomial
            crc &= 0xFFFF
        
        return crc