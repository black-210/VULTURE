"""RF-DNA v3: deterministic RF simulation and fingerprinting primitives.

This package is intentionally hardware-agnostic. It supports safe, local,
receive-oriented analysis and does not implement transmission or jamming.
"""

from .fingerprint import Fingerprint, extract_fingerprint, similarity
from .simulator import generate_iq

__all__ = ["Fingerprint", "extract_fingerprint", "similarity", "generate_iq"]
