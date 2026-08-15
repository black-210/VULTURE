from typing import Optional


def detect_gpu() -> Optional[str]:
    """Detect available GPU device string. Returns like 'cuda:0' or None."""
    try:
        import torch
        if torch.cuda.is_available():
            return f"cuda:{torch.cuda.current_device()}"
        return None
    except Exception:
        try:
            import cupy as cp  # type: ignore
            return "cupy"
        except Exception:
            return None
