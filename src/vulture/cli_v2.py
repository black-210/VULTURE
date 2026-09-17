"""Compatibility entry point for the former v2 CLI.

The old v2 file displayed simulated offensive output. It now delegates to the
safe, truthful general CLI while preserving ``python -m vulture.cli_v2``.
"""
from .cli import InteractiveShell, cli

VulturePrompt = InteractiveShell

__all__ = ["InteractiveShell", "VulturePrompt", "cli"]

if __name__ == "__main__":
    cli()
