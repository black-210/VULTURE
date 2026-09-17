"""🦅 VULTURE - Autonomous Intelligence & Research Platform"""

__version__ = "0.1.0"
__author__ = "BLACK Cyber Falcon"
__license__ = "Apache-2.0"

from vulture.chemical_rf import ChemicalBond, ChemicalEquationSolver, MolecularRFAnalyzer, NMRPeak
from vulture.core import FrameworkRegistry, ConfigManager, PermissionManager

__all__ = [
    "FrameworkRegistry", "ConfigManager", "PermissionManager",
    "ChemicalBond", "ChemicalEquationSolver", "MolecularRFAnalyzer", "NMRPeak",
]
