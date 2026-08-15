from typing import Any, Dict

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None


def compute_psd(samples: Any, method: str = "welch") -> Dict[str, Any]:
    """Compute PSD using the chosen method (placeholder)."""
    if np is None:
        raise RuntimeError("numpy is required for PSD computation")
    # TODO: implement welch/periodogram/multitaper options
    return {"freqs": None, "psd": None}
