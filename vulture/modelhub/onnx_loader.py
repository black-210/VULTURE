"""
ONNX loader utility (uses onnxruntime if available).
"""
from typing import Optional

try:
    import onnxruntime as ort
except Exception:
    ort = None


def load_onnx(path: str) -> Optional[object]:
    """Return an onnxruntime.InferenceSession or None if not available."""
    if ort is None:
        return None
    return ort.InferenceSession(path)
