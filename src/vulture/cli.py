"""Click-based CLI with all commands."""

import click
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def cli(verbose):
    """🦅 VULTURE - Intelligence & Research Platform CLI."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')


@cli.command()
def info():
    """Show platform information."""
    click.echo("🦅 VULTURE v0.1.0")
    click.echo("Framework: Production-grade Intelligence & Research")
    click.echo("Author: BLACK Cyber Falcon")
    click.echo("License: AGPL-3.0")
    click.echo("")
    click.echo("Available Commands:")
    click.echo("  sdr     - SDR/IQ operations")
    click.echo("  rf      - RF analysis")
    click.echo("  ml      - Machine learning")
    click.echo("  dsp     - Signal processing")
    click.echo("  gui     - Launch GUI")


@cli.group()
def sdr():
    """SDR/IQ operations."""
    pass


@sdr.command()
@click.option('--device', default='rtlsdr', help='Device type: rtlsdr, uhd, pluto')
@click.option('--freq', type=float, default=2.4e9, help='Center frequency (Hz)')
@click.option('--rate', type=float, default=2e6, help='Sample rate (Hz)')
@click.option('--samples', type=int, default=1000000, help='Number of samples')
@click.option('--output', default='recording.npy', help='Output file')
def record(device, freq, rate, samples, output):
    """Record IQ data from SDR."""
    try:
        from vulture.sdr_iq_framework import HardwareAbstraction, IQRecorder
        
        click.echo(f"Opening {device} device...")
        hw = HardwareAbstraction(device)
        hw.open_device()
        hw.set_center_freq(freq)
        hw.set_sample_rate(rate)
        hw.set_gain('auto')
        
        click.echo(f"Recording {samples} samples...")
        data = hw.read_samples(samples)
        hw.close_device()
        
        recorder = IQRecorder(output, rate, freq)
        recorder.append_samples(data)
        recorder.save(format='npy')
        
        click.echo(f"✓ Saved to {output}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)


@cli.group()
def rf():
    """RF analysis."""
    pass


@rf.command()
@click.option('--input', required=True, help='Input file')
@click.option('--fft-size', type=int, default=1024, help='FFT size')
def analyze(input, fft_size):
    """Analyze RF signal."""
    try:
        import numpy as np
        from vulture.rf_intelligence import FFTAnalyzer
        
        data = np.load(input)
        analyzer = FFTAnalyzer(fft_size=fft_size)
        freqs, mags = analyzer.compute_fft(data)
        
        click.echo(f"✓ FFT Analysis:")
        click.echo(f"  Peak frequency: {freqs[np.argmax(mags)]:.2e} Hz")
        click.echo(f"  Peak magnitude: {np.max(mags):.4f}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)


@cli.group()
def ml():
    """Machine learning."""
    pass


@ml.command()
@click.option('--input', required=True, help='Training data')
@click.option('--output', default='model.pkl', help='Model path')
@click.option('--model-type', default='rf', help='Model type: rf, svm, mlp')
def train(input, output, model_type):
    """Train ML model."""
    try:
        import numpy as np
        from vulture.ml_framework import ModelTrainer
        
        click.echo(f"Loading data: {input}")
        data = np.load(input)
        X, y = data[:, :-1], data[:, -1]
        
        click.echo(f"Training {model_type} model...")
        trainer = ModelTrainer(model_type=model_type, task='classification')
        trainer.train(X, y)
        trainer.save(output)
        
        click.echo(f"✓ Model saved to {output}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)


@cli.group()
def dsp():
    """Signal processing."""
    pass


@dsp.command()
@click.option('--input', required=True, help='Input signal')
@click.option('--order', type=int, default=64, help='Filter order')
@click.option('--cutoff', type=float, default=0.1, help='Cutoff frequency')
def filter(input, order, cutoff):
    """Design and apply FIR filter."""
    try:
        import numpy as np
        from vulture.signal_processing import Filters
        
        data = np.load(input)
        b = Filters.design_fir(order, cutoff)
        filtered = Filters.apply_fir(data, b)
        
        click.echo(f"✓ Filtered {len(data)} samples")
        click.echo(f"  Filter order: {order}")
        click.echo(f"  Cutoff: {cutoff}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)


@cli.command()
def gui():
    """Launch GUI application."""
    try:
        from vulture.gui import launch_gui
        launch_gui()
    except Exception as e:
        click.echo(f"✗ GUI failed: {e}", err=True)


if __name__ == '__main__':
    cli()
