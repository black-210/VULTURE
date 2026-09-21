"""VULTURE public package metadata and compatibility exports."""

__version__ = "3.0.0"
__author__ = "BLACK Cyber Falcon"
__license__ = "AGPL-3.0-or-later"

from vulture.chemical_rf import ChemicalBond, ChemicalEquationSolver, MolecularRFAnalyzer, NMRPeak
from vulture.core import ConfigManager, FrameworkRegistry, PermissionManager

__all__ = [
    "FrameworkRegistry",
    "ConfigManager",
    "PermissionManager",
    "ChemicalBond",
    "ChemicalEquationSolver",
    "MolecularRFAnalyzer",
    "NMRPeak",
]
