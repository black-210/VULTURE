from click.testing import CliRunner

from vulture.cli import cli


def test_interactive_option_welcomes_and_exits(monkeypatch):
    # The shell is tested independently so no terminal is required.
    from vulture.cli import InteractiveShell
    shell = InteractiveShell()
    shell.process("status")
    assert shell.history == ["status"]
    shell.process("exit")
    assert shell.running is False


def test_science_commands_are_real_calculations():
    result = CliRunner().invoke(cli, ["rf-wavelength", "--frequency-hz", "1e9"])
    assert result.exit_code == 0
    assert "0.299792458" in result.output


def test_chemical_rf_command_routes_to_real_subcommand():
    result = CliRunner().invoke(cli, ["chemical-rf", "nmr", "--nucleus", "1H", "--field-t", "7"])
    assert result.exit_code == 0
    assert "frequency_hz" in result.output
