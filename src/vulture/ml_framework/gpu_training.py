"""GPU training support."""
import numpy as np
import logging
logger = logging.getLogger(__name__)
class GPUTraining:
    def __init__(self):
        self.gpu_available = False
        try:
            import torch
            self.torch = torch
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.gpu_available = self.device.type == 'cuda'
            logger.info(f"GPU training initialized on {self.device}")
        except:
            logger.warning("PyTorch not available")
    def to_gpu(self, data):
        if self.gpu_available and hasattr(data, 'to'):
            return data.to(self.device)
        return data
    def to_cpu(self, data):
        if hasattr(data, 'cpu'):
            return data.cpu()
        return data
    def get_device_info(self):
        if self.gpu_available:
            return {'device': str(self.device), 'cuda_available': True}
        return {'device': 'cpu', 'cuda_available': False}