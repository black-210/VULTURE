from click.testing import CliRunner
from vulture.forensic_cli import forensic_cli


def test_physics_forensic_report_json_and_file(tmp_path):
    output = tmp_path / "case.json"
    result = CliRunner().invoke(forensic_cli, ["physics", "--case-id", "C-1", "--subject", "capture", "--frequency-hz", "0", "--distance-m", "10", "--output", str(output)])
    assert result.exit_code == 0
    assert "PHY-001" in result.output
    assert output.exists()


def test_protocol_mismatch_is_reported_as_evidence():
    result = CliRunner().invoke(forensic_cli, ["protocol", "--case-id", "C-2", "--subject", "frame", "--frames-json", '[{"length": 4, "declared_length": 5}]', "--format", "txt"])
    assert result.exit_code == 0
    assert "PROTO-001" in result.output
    assert "declared=5" in result.output
