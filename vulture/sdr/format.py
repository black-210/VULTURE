from typing import Optional

def detect_format(path: str) -> Optional[str]:
    """Naive format detection based on file extension."""
    if path.endswith(".npy"):
        return "npy"
    if path.endswith(".bin"):
        return "bin"
    if path.endswith(".wav"):
        return "wav"
    return None
