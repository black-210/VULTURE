from click.testing import CliRunner

from vulture.cli import cli


def test_interactive_help_and_exit():
    shell = __import__("vulture.cli", fromlist=["InteractiveShell"]).InteractiveShell()
    shell.process("help")
    assert shell.history[-1] == "help"
    shell.process("exit")
    assert shell.running is False


def test_rf_wavelength_and_forensic_math_are_real():
    runner = CliRunner()
    result = runner.invoke(cli, ["rf-wavelength", "--frequency-hz", "1e9"])
    assert result.exit_code == 0
    assert "wavelength_m" in result.output

    forensic = runner.invoke(cli, ["forensic", "math", "--case-id", "M-1", "--subject", "demo", "--matrix-json", "[[2,1],[1,1]]", "--vector-json", "[3,2]"])
    assert forensic.exit_code == 0
    assert "case_id" in forensic.output
