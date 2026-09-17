"""VULTURE CLI with truthful, offline science and forensic capabilities.

The interactive prompt is intentionally a friendly ``>`` shell that exposes
real, local calculations and forensic audit checks. It does not scan live
systems, transmit RF, or attack targets.
"""
from __future__ import annotations

import json
import shlex
from typing import Any

import click

from vulture.chemical_rf.science import free_space_path_loss_db, wavelength_m
from vulture.chemical_rf.spectroscopy import larmor_frequency_hz
from vulture.forensics import audit_chemistry, audit_mathematics, audit_physics, audit_protocol


@click.group(invoke_without_command=True)
@click.option("--interactive", is_flag=True, help="Open the interactive > prompt.")
@click.pass_context
def cli(ctx: click.Context, interactive: bool) -> None:
    """🦅 VULTURE — offline RF, chemistry, physics, mathematics and evidence audit CLI."""
    if interactive:
        InteractiveShell().run()
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
def info() -> None:
    """Display platform capabilities."""
    click.echo("🦅 VULTURE")
    click.echo("Science: chemistry • physics • mathematics • RF")
    click.echo("Forensics: offline audit of supplied evidence only")
    click.echo("Interactive: vulture --interactive")


@cli.command()
def status() -> None:
    """Show safe runtime status."""
    payload = {
        "cli": "online",
        "mode": "offline-deterministic",
        "hardware": "not-opened",
        "network": "disabled",
        "rf_transmit": "disabled",
        "analysis": "local-only",
    }
    click.echo(json.dumps(payload, indent=2, sort_keys=True))


@cli.command("rf-wavelength")
@click.option("--frequency-hz", required=True, type=float)
def rf_wavelength(frequency_hz: float) -> None:
    """Calculate wavelength from frequency."""
    click.echo(json.dumps({"frequency_hz": frequency_hz, "wavelength_m": wavelength_m(frequency_hz)}, indent=2))


@cli.command("rf-path-loss")
@click.option("--frequency-hz", required=True, type=float)
@click.option("--distance-m", required=True, type=float)
def rf_path_loss(frequency_hz: float, distance_m: float) -> None:
    """Calculate free-space path loss for supplied parameters only."""
    click.echo(json.dumps({"frequency_hz": frequency_hz, "distance_m": distance_m, "path_loss_db": free_space_path_loss_db(frequency_hz, distance_m)}, indent=2))


@cli.command("chemical-rf")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def chemical_rf(args: tuple[str, ...]) -> None:
    """Route to the Chemical-RF command group."""
    from vulture.chemical_rf.cli import chemical_rf_cli

    if not args:
        click.echo(chemical_rf_cli.get_help(click.Context(chemical_rf_cli)))
        return
    chemical_rf_cli.main(list(args), standalone_mode=False)


@cli.group("forensic")
def forensic() -> None:
    """Offline evidence audit commands for supplied local data."""


@forensic.command("physics")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--distance-m", required=True, type=float)
@click.option("--bandwidth-hz", type=float, default=None)
@click.option("--output", type=click.Path(dir_okay=False), default=None)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def forensic_physics(case_id: str, subject: str, frequency_hz: float, distance_m: float, bandwidth_hz: float | None, output: str | None, fmt: str) -> None:
    """Audit local physical measurement metadata."""
    report = audit_physics(case_id, subject, frequency_hz=frequency_hz, distance_m=distance_m, bandwidth_hz=bandwidth_hz)
    if output:
        from vulture.forensics import write_report
        write_report(report, output, fmt)
    click.echo(report.to_json() if fmt == "json" else report.to_text())


@forensic.command("chemistry")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--compounds-json", required=True)
def forensic_chemistry(case_id: str, subject: str, compounds_json: str) -> None:
    """Audit local compound composition structures."""
    compounds = json.loads(compounds_json)
    report = audit_chemistry(case_id, subject, compounds)
    click.echo(report.to_json())


@forensic.command("math")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--matrix-json", required=True)
@click.option("--vector-json", required=True)
def forensic_math(case_id: str, subject: str, matrix_json: str, vector_json: str) -> None:
    """Audit a local linear system."""
    matrix = json.loads(matrix_json)
    vector = json.loads(vector_json)
    report = audit_mathematics(case_id, subject, matrix, vector)
    click.echo(report.to_json())


@forensic.command("protocol")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frames-json", required=True)
@click.option("--output", type=click.Path(dir_okay=False), default=None)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def forensic_protocol(case_id: str, subject: str, frames_json: str, output: str | None, fmt: str) -> None:
    """Audit supplied protocol/frame metadata without network access."""
    frames = json.loads(frames_json)
    report = audit_protocol(case_id, subject, frames)
    if output:
        from vulture.forensics import write_report
        write_report(report, output, fmt)
    click.echo(report.to_json() if fmt == "json" else report.to_text())


class InteractiveShell:
    """Friendly interactive prompt for the scientific and forensic toolset."""

    def __init__(self) -> None:
        self.running = True
        self.history: list[str] = []

    @staticmethod
    def banner() -> None:
        click.echo("══════════════════════════════════════════════════════════")
        click.echo("🦅 VULTURE — Offline Scientific Intelligence Platform")
        click.echo("chemistry • physics • mathematics • RF • forensic audit")
        click.echo("Type: help | status | forensic physics | exit")
        click.echo("══════════════════════════════════════════════════════════")

    def run(self) -> None:
        self.banner()
        while self.running:
            try:
                cmd = click.prompt(">", prompt_suffix=" ", show_default=False)
            except (EOFError, KeyboardInterrupt):
                click.echo()
                break
            self.process(cmd)

    def process(self, line: str) -> None:
        line = line.strip()
        if not line:
            return
        self.history.append(line)
        command = line.lower()
        if command in {"exit", "quit"}:
            self.running = False
            click.echo("✓ Session closed safely.")
            return
        if command in {"help", "?"}:
            click.echo("Available commands:")
            click.echo("  info")
            click.echo("  status")
            click.echo("  rf-wavelength --frequency-hz 1e9")
            click.echo("  rf-path-loss --frequency-hz 2.4e9 --distance-m 10")
            click.echo("  chemical-rf nmr --nucleus 1H --field-t 7")
            click.echo("  forensic physics --case-id C-001 --subject capture --frequency-hz 2.4e9 --distance-m 10")
            click.echo("  forensic chemistry --case-id C-002 --subject sample --compounds-json '[{\"elements\":{\"H\":2,\"O\":1}}]' ")
            click.echo("  forensic math --case-id C-003 --subject system --matrix-json '[[2,1],[1,1]]' --vector-json '[3,2]' ")
            click.echo("  forensic protocol --case-id C-004 --subject frame --frames-json '[{\"length\":4,\"declared_length\":5}]'")
            click.echo("  history")
            click.echo("  exit")
            return
        if command == "history":
            for index, item in enumerate(self.history[:-1], 1):
                click.echo(f"{index}: {item}")
            return
        try:
            cli.main(shlex.split(line), standalone_mode=False)
        except SystemExit:
            pass
        except Exception as exc:  # pragma: no cover
            click.echo(f"error: {exc}")


if __name__ == "__main__":
    cli()
