from click.testing import CliRunner

from vulture.cli import cli


def test_lab_simulation_is_explicit_and_non_operational():
    result = CliRunner().invoke(cli, ["lab", "attack-sim", "--scenario", "spoofing"])
    assert result.exit_code == 0
    assert "AUTHORIZED_OFFLINE_LAB" in result.output
    assert "no_network" in result.output
    assert "transmission" in result.output


def test_defense_simulation_produces_auditable_result():
    result = CliRunner().invoke(cli, ["lab", "defense-sim", "--scenario", "jamming-detection"])
    assert result.exit_code == 0
    assert "evidence_sha256" in result.output
    assert "automatic_transmit" in result.output
