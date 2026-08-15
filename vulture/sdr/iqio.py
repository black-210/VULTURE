from typing import Optional, Any

class IQRecorder:
    """Record IQ samples to file formats (NPY, BIN, WAV)."""

    def __init__(self, out_path: str):
        self.out_path = out_path

    def record(self, samples) -> str:
        """Persist samples and return path."""
        # TODO: implement write logic depending on format
        return self.out_path

class IQPlayer:
    """Playback IQ samples from file."""

    def __init__(self, src_path: str):
        self.src_path = src_path

    def play(self):
        """Yield samples for processing."""
        # TODO: implement reading logic
        yield from ()
