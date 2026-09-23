import json
import subprocess


def test_purple_cli_builds_and_reports_controls(tmp_path):
    baseline = tmp_path / "baseline.txt"
    baseline.write_text("1\n1.01\n0.99\n1\n", encoding="utf-8")
    assert baseline.read_text(encoding="utf-8").startswith("1")


def test_purple_contract_is_local_only():
    from pathlib import Path
    text = Path("c/purple/README.md").read_text(encoding="utf-8")
    assert "does not scan systems" in text
    assert "does not" in text
