"""Small, dependency-light offline analysis toolkit used by VULTURE."""
from .audit import audit_values
from .peaks import find_peaks
from .spectral import dominant_frequency
from .stats import describe
from .workflow import analyze

__all__ = ["analyze", "audit_values", "describe", "dominant_frequency", "find_peaks"]
