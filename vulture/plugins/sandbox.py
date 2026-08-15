"""
Simple plugin sandbox runner using subprocess with optional resource limits on Unix.
This MVP intentionally keeps the model simple: it spawns the plugin as a separate process,
captures stdout/stderr, and enforces a timeout.
"""
import subprocess
import sys
import os
from typing import Tuple, Optional

try:
    import resource  # Unix only
except Exception:
    resource = None


def _limit_resources(memory_bytes: int = 256 * 1024 * 1024):
    # Called in child process before exec on Unix
    if resource is None:
        return
    # RLIMIT_AS limits total address space
    try:
        resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
    except Exception:
        pass


def run_plugin(command: list, timeout: int = 10, memory_limit_bytes: Optional[int] = None) -> Tuple[int, str, str]:
    """Run a plugin command list in a sandboxed subprocess.

    Returns (returncode, stdout, stderr)
    """
    preexec_fn = None
    if resource is not None and memory_limit_bytes is not None:
        def _pre():
            _limit_resources(memory_limit_bytes)
        preexec_fn = _pre

    try:
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False, preexec_fn=preexec_fn)
        stdout = proc.stdout.decode('utf-8', errors='replace')
        stderr = proc.stderr.decode('utf-8', errors='replace')
        return proc.returncode, stdout, stderr
    except subprocess.TimeoutExpired as e:
        return -1, '', f'TimeoutExpired: {e}'
    except Exception as e:
        return -2, '', str(e)
