"""VULTURE command line interface.

The CLI is intentionally offline-first: chemistry, physics, mathematics, RF
and report commands calculate values from explicit inputs. Hardware/network
operations are not started implicitly. ``vulture --interactive`` provides a
friendly ``>`` prompt and routes commands through the same Click command tree.
"""
from __future__ import annotations

import json
import shlex
from typing import Iterable

import click


def _emit(value: object) -> None:
    click.echo(json.dumps(value, indent=2, sort_keys=True, default=str))


@click.group(invoke_without_command=True)
@click.option("--interactive", is_flag=True, help="Open the interactive > prompt.")
@click.pass_context
def cli(ctx: click.Context, interactive: bool) -> None:
    """🦅 VULTURE — scientific RF, chemistry, physics and mathematics CLI."""
    if interactive:
        InteractiveShell().run()
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
def info() -> None:
    """Display the installed VULTURE capabilities."""
    click.echo("🦅 VULTURE Scientific Intelligence Platform")
    click.echo("Offline analysis: chemistry • physics • mathematics • RF • provenance")
    click.echo("Interactive mode: vulture --interactive")


@cli.command()
@click.option("--device", default="simulator", show_default=True)
def sdr(device: str) -> None:
    """Describe an SDR backend without opening hardware."""
    _emit({"device": device, "mode": "description-only", "hardware_opened": False})


@cli.command()
def rf() -> None:
    """Show RF analysis commands."""
    click.echo("RF commands: rf-wavelength, rf-path-loss, chemical-rf report")


@cli.command()
def ml() -> None:
    """Show ML integration status without pretending to run inference."""
    _emit({"component": "ML", "status": "available-for-integration", "model_loaded": False})


@cli.command()
def dsp() -> None:
    """Show DSP analysis commands."""
    click.echo("DSP commands: chemical-rf nmr, FID simulation, FFT spectrum")


@cli.command()
def gui() -> None:
    """Describe GUI availability without launching a display unexpectedly."""
    click.echo("GUI launcher is intentionally explicit; use the platform GUI module.")


@cli.command("rf-wavelength")
@click.option("--frequency-hz", required=True, type=click.FloatRange(min=0, min_open=True))
def rf_wavelength(frequency_hz: float) -> None:
    """Calculate wavelength from frequency using c/f."""
    from vulture.chemical_rf.science import wavelength_m
    _emit({"frequency_hz": frequency_hz, "wavelength_m": wavelength_m(frequency_hz)})


@cli.command("rf-path-loss")
@click.option("--frequency-hz", required=True, type=click.FloatRange(min=0, min_open=True))
@click.option("--distance-m", required=True, type=click.FloatRange(min=0, min_open=True))
def rf_path_loss(frequency_hz: float, distance_m: float) -> None:
    """Calculate free-space path loss; this never transmits RF."""
    from vulture.chemical_rf.science import free_space_path_loss_db
    _emit({"frequency_hz": frequency_hz, "distance_m": distance_m, "path_loss_db": free_space_path_loss_db(frequency_hz, distance_m)})


@cli.command("chemical-rf")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def chemical_rf(args: tuple[str, ...]) -> None:
    """Run Chemical-RF subcommands (nmr, material, physics, report)."""
    from vulture.chemical_rf.cli import chemical_rf_cli
    if not args:
        click.echo(chemical_rf_cli.get_help(click.Context(chemical_rf_cli)))
        return
    try:
        chemical_rf_cli.main(list(args), standalone_mode=False)
    except click.ClickException as exc:
        raise click.ClickException(str(exc)) from exc


class InteractiveShell:
    """Interactive command shell backed by the same public CLI commands."""

    def __init__(self) -> None:
        self.running = True
        self.history: list[str] = []

    @staticmethod
    def welcome() -> None:
        click.echo("╔══════════════════════════════════════════════════════════════╗")
        click.echo("║ 🦅 VULTURE Scientific Intelligence Platform                 ║")
        click.echo("║ Chemistry • Physics • Mathematics • RF • Audit              ║")
        click.echo("║ Type help for commands, exit to leave                       ║")
        click.echo("╚══════════════════════════════════════════════════════════════╝")

    def run(self) -> None:
        self.welcome()
        while self.running:
            try:
                line = click.prompt(">", prompt_suffix=" ", default="", show_default=False)
            except (EOFError, KeyboardInterrupt):
                click.echo()
                break
            self.process(line)

    def process(self, line: str) -> None:
        line = line.strip()
        if not line:
            return
        if line.lower() in {"exit", "quit"}:
            self.running = False
            click.echo("✓ Session closed safely.")
            return
        if line.lower() == "history":
            for index, command in enumerate(self.history, 1):
                click.echo(f"{index}: {command}")
            return
        if line.lower() in {"help", "?"}:
            click.echo("Commands: info, chemical-rf, rf-wavelength, rf-path-loss, status, history, exit")
            click.echo("Example: chemical-rf nmr --nucleus 1H --field-t 7")
            return
        self.history.append(line)
        try:
            cli.main(shlex.split(line), standalone_mode=False)
        except click.ClickException as exc:
            click.echo(f"error: {exc.format_message()}", err=True)
        except SystemExit:
            pass


@cli.command()
def status() -> None:
    """Show truthful runtime status; no fake device counts or progress bars."""
    _emit({"cli": "online", "interactive_prompt": True, "hardware": "not opened", "network": "not used", "analysis": "offline deterministic"})


if __name__ == "__main__":
    cli()
