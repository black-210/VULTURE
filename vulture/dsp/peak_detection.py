"""
Peak detection utilities using scipy.signal.find_peaks with numpy fallback.
"""
from typing import Any, Dict, List, Optional

try:
    import numpy as np
except Exception:
    np = None


def detect_peaks(data: Any, method: str = "prominence", height: Optional[float] = None, distance: Optional[int] = None, prominence: Optional[float] = None) -> Dict[str, Any]:
    """Detect peaks in 1D data.

    Returns:
        {'peaks': indices, 'properties': properties}
    """
    if np is None:
        raise RuntimeError("numpy is required for peak detection")

    arr = np.asarray(data)
    try:
        from scipy.signal import find_peaks

        kwargs = {}
        if height is not None:
            kwargs['height'] = height
        if distance is not None:
            kwargs['distance'] = distance
        if prominence is not None:
            kwargs['prominence'] = prominence

        peaks, props = find_peaks(arr, **kwargs)
        return {"peaks": peaks.tolist(), "properties": {k: v.tolist() if hasattr(v, 'tolist') else v for k, v in props.items()}}
    except Exception:
        # Fallback: simple threshold-based peaks
        if height is None:
            height = float(arr.mean() + arr.std())
        peaks = [int(i) for i in range(1, len(arr) - 1) if arr[i] > arr[i - 1] and arr[i] > arr[i + 1] and arr[i] > height]
        return {"peaks": peaks, "properties": {}}
