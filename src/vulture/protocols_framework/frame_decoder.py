"""Frame decoding."""

import numpy as np
import logging

logger = logging.getLogger(__name__)

class FrameDecoder:
    """Decode communication frames."""
    
    def __init__(self):
        self.frame_definitions = {}
    
    def define_frame(self, name, structure):
        """Define frame structure."""
        self.frame_definitions[name] = structure
        logger.info(f"Frame definition registered: {name}")
    
    def decode_frame(self, data, frame_name):
        """Decode frame data."""
        if frame_name not in self.frame_definitions:
            return None
        
        frame_def = self.frame_definitions[frame_name]
        decoded = {}
        offset = 0
        
        for field_name, field_len in frame_def.items():
            field_data = data[offset:offset+field_len]
            decoded[field_name] = field_data
            offset += field_len
        
        return decoded
    
    def validate_frame(self, data, frame_name):
        """Validate frame format."""
        if frame_name not in self.frame_definitions:
            return False
        
        expected_length = sum(self.frame_definitions[frame_name].values())
        return len(data) >= expected_length
    
    def extract_payload(self, frame_data, payload_field):
        """Extract payload from frame."""
        return frame_data.get(payload_field)