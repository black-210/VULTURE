import os
from vulture.plugins.sandbox import run_plugin


def test_run_plugin_echo(tmp_path):
    script = tmp_path / "echo.py"
    script.write_text('print("hello-sandbox")')
    rc, out, err = run_plugin(["/usr/bin/env", "python3", str(script)], timeout=5)
    assert rc == 0
    assert "hello-sandbox" in out
