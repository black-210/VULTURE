from typing import Any, Optional


def to_torch_tensor(X: Any, device: Optional[str] = None):
    try:
        import torch
        t = torch.as_tensor(X)
        if device:
            try:
                t = t.to(device)
            except Exception:
                pass
        return t
    except Exception:
        return X


def save_model_onnx(model: Any, path: str, example_input: Optional[Any] = None) -> bool:
    """Attempt to export a PyTorch model to ONNX. Returns True on success."""
    try:
        import torch
        if not hasattr(model, "forward"):
            return False
        if example_input is None:
            # cannot export without an example input
            return False
        torch.onnx.export(model, example_input, path)
        return True
    except Exception:
        return False
