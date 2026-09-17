"""Dual-use authorized laboratory commands for VULTURE."""
from __future__ import annotations

import json
import click

from .lab import attack_simulation, defense_simulation


def _print(result) -> None:
    click.echo(json.dumps(result.to_dict(), indent=2, sort_keys=True))


@click.group("lab")
def lab_cli() -> None:
    """Authorized red-team/blue-team simulations using synthetic local data."""


@lab_cli.command("attack-sim")
@click.option("--scenario", type=click.Choice(["rf-jamming", "spoofing", "injection", "protocol-abuse"]), required=True)
@click.option("--seed", type=int, default=7, show_default=True)
def attack_sim(scenario: str, seed: int) -> None:
    """Simulate an offensive scenario; no target, network, or transmitter is used."""
    _print(attack_simulation(scenario, seed))


@lab_cli.command("defense-sim")
@click.option("--scenario", type=click.Choice(["jamming-detection", "spoof-detection", "protocol-anomaly", "chemical-rf-drift"]), required=True)
@click.option("--seed", type=int, default=11, show_default=True)
def defense_sim(scenario: str, seed: int) -> None:
    """Simulate detection and response against synthetic telemetry."""
    _print(defense_simulation(scenario, seed))
