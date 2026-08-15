"""Protocol parsing and dissection."""

import numpy as np
import logging

logger = logging.getLogger(__name__)

class ProtocolParser:
    """Parse communication protocols."""
    
    def __init__(self):
        self.protocols = {}
        self.packet_definitions = {}
    
    def register_protocol(self, name, definition):
        """Register protocol definition."""
        self.protocols[name] = definition
        logger.info(f"Protocol registered: {name}")
    
    def parse_packet(self, data, protocol_name):
        """Parse packet according to protocol."""
        if protocol_name not in self.protocols:
            logger.error(f"Protocol not found: {protocol_name}")
            return None
        
        protocol_def = self.protocols[protocol_name]
        parsed = {}
        offset = 0
        
        for field_name, field_type in protocol_def.items():
            if field_type == 'uint8':
                parsed[field_name] = data[offset]
                offset += 1
            elif field_type == 'uint16':
                parsed[field_name] = int.from_bytes(data[offset:offset+2], 'big')
                offset += 2
            elif field_type == 'uint32':
                parsed[field_name] = int.from_bytes(data[offset:offset+4], 'big')
                offset += 4
        
        return parsed
    
    def extract_fields(self, data, field_sizes):
        """Extract fields from binary data."""
        fields = []
        offset = 0
        
        for size in field_sizes:
            field_data = data[offset:offset+size]
            fields.append(field_data)
            offset += size
        
        return fields
    
    def detect_protocol_type(self, data):
        """Auto-detect protocol type from header."""
        if len(data) < 4:
            return None
        
        magic = data[0:4]
        # Simple magic number detection
        protocol_map = {
            b'\x00\x01\x02\x03': 'CUSTOM_A',
            b'\xFF\xEE\xDD\xCC': 'CUSTOM_B',
        }
        
        return protocol_map.get(magic, 'UNKNOWN')