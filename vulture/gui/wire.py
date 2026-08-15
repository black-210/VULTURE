"""
GUI wiring helpers (minimal): connect analyzers to GUI panels (placeholders).
This file provides convenience functions to wire the PyQt GUI to backend analyzers for demos.
"""
from typing import Any


def wire_gui_to_backend(gui_app: Any, analyzer: Any = None, visualizer: Any = None):
    """Wire GUI components to backend objects. This is a placeholder to show expected hooks.

    Arguments:
        gui_app: the main GUI application object (PyQt app or custom container)
        analyzer: RealTimeAnalyzer instance
        visualizer: SpectrumVisualizer instance
    """
    # Example (pseudo-code):
    # gui_app.spectrum_panel.on_new_frame = analyzer.process_frame
    # gui_app.spectrum_panel.render = visualizer.render_spectrum
    try:
        if hasattr(gui_app, 'spectrum_panel') and analyzer is not None:
            gui_app.spectrum_panel.process_frame = analyzer.process_frame
        if hasattr(gui_app, 'spectrum_panel') and visualizer is not None:
            gui_app.spectrum_panel.render = visualizer.render_spectrum
    except Exception:
        # best-effort wiring; do not fail if GUI is not present
        pass
