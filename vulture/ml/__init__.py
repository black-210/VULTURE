"""
Machine Learning & Deep Learning framework stubs.
Preprocessing, feature engineering, training wrappers, validation, and PyTorch helpers.
"""
from .preprocess import scale_minmax, standardize, to_tensor
from .features import extract_basic_features
from .training import Trainer
from .validation import compute_metrics
from .pytorch import to_torch_tensor, save_model_onnx
from .gpu import detect_gpu

__all__ = [
    "scale_minmax",
    "standardize",
    "to_tensor",
    "extract_basic_features",
    "Trainer",
    "compute_metrics",
    "to_torch_tensor",
    "save_model_onnx",
    "detect_gpu",
]
