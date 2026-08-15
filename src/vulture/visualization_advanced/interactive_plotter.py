"""Interactive plotter."""

import numpy as np
import logging

logger = logging.getLogger(__name__)

class InteractivePlotter:
    """Interactive plotting utilities."""
    
    def __init__(self):
        self.plots = {}
        self.current_limits = {}
    
    def create_plot(self, plot_id, plot_type='line'):
        """Create new plot."""
        self.plots[plot_id] = {'type': plot_type, 'data': []}
    
    def add_data_to_plot(self, plot_id, x, y, label=None):
        """Add data to plot."""
        if plot_id not in self.plots:
            self.create_plot(plot_id)
        
        self.plots[plot_id]['data'].append({
            'x': x,
            'y': y,
            'label': label
        })
    
    def set_plot_limits(self, plot_id, xlim=None, ylim=None):
        """Set plot axis limits."""
        self.current_limits[plot_id] = {'xlim': xlim, 'ylim': ylim}
    
    def get_plot_data(self, plot_id):
        """Retrieve plot data."""
        return self.plots.get(plot_id)
    
    def pan_plot(self, plot_id, dx, dy):
        """Pan plot."""
        if plot_id in self.current_limits:
            limits = self.current_limits[plot_id]
            if limits['xlim']:
                limits['xlim'] = (limits['xlim'][0] + dx, limits['xlim'][1] + dx)
    
    def zoom_plot(self, plot_id, zoom_factor, center=None):
        """Zoom plot."""
        if plot_id in self.current_limits:
            limits = self.current_limits[plot_id]
            if limits['xlim']:
                xlim = limits['xlim']
                new_width = (xlim[1] - xlim[0]) / zoom_factor
                if center is None:
                    center = (xlim[0] + xlim[1]) / 2
                limits['xlim'] = (center - new_width/2, center + new_width/2)