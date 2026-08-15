"""Packet analysis."""

import numpy as np
import logging

logger = logging.getLogger(__name__)

class PacketAnalyzer:
    """Analyze communication packets."""
    
    def __init__(self):
        self.packets = []
    
    def detect_packets(self, data, threshold=0.3):
        """Detect packet boundaries."""
        envelope = np.abs(data)
        mean_env = np.mean(envelope)
        threshold_val = mean_env * threshold
        
        above_threshold = envelope > threshold_val
        packets = []
        in_packet = False
        start = 0
        
        for i, is_active in enumerate(above_threshold):
            if is_active and not in_packet:
                in_packet = True
                start = i
            elif not is_active and in_packet:
                in_packet = False
                packets.append((start, i))
        
        return packets
    
    def extract_packet_data(self, data, packet_bounds):
        """Extract data for detected packets."""
        packet_list = []
        for start, end in packet_bounds:
            packet_data = data[start:end]
            packet_list.append({
                'data': packet_data,
                'start': start,
                'end': end,
                'length': end - start,
                'power': np.mean(np.abs(packet_data)**2)
            })
        return packet_list
    
    def analyze_packet_timing(self, packets):
        """Analyze timing between packets."""
        if len(packets) < 2:
            return {}
        
        intervals = []
        for i in range(len(packets)-1):
            interval = packets[i+1]['start'] - packets[i]['end']
            intervals.append(interval)
        
        return {
            'mean_interval': np.mean(intervals),
            'std_interval': np.std(intervals),
            'min_interval': np.min(intervals),
            'max_interval': np.max(intervals),
            'intervals': intervals
        }