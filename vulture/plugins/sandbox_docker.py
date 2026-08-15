"""
Docker-based plugin sandbox shim.
Attempts to run a plugin inside a Docker container (if docker is available) and falls back to process-based sandbox.
"""
import shutil
import subprocess
import os
from typing import Tuple, Optional

from .sandbox import run_plugin


def run_plugin_docker(image: str, command: list, timeout: int = 30, mounts: Optional[list] = None) -> Tuple[int, str, str]:
    """Run plugin in docker container if available.

    Args:
        image: docker image to run
        command: list of command args to run inside container
        timeout: timeout in seconds
        mounts: list of (host_path, container_path, mode) tuples
    Returns:
        (returncode, stdout, stderr)
    """
    docker_bin = shutil.which('docker')
    if docker_bin is None:
        # fallback to process sandbox
        return run_plugin(command, timeout=timeout)

    # build docker run command
    cmd = [docker_bin, 'run', '--rm']
    if mounts:
        for host_p, cont_p, mode in mounts:
            cmd.extend(['-v', f'{host_p}:{cont_p}:{mode}'])
    cmd.append(image)
    cmd.extend(command)

    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False)
        stdout = proc.stdout.decode('utf-8', errors='replace')
        stderr = proc.stderr.decode('utf-8', errors='replace')
        return proc.returncode, stdout, stderr
    except subprocess.TimeoutExpired as e:
        return -1, '', f'TimeoutExpired: {e}'
    except Exception as e:
        return -2, '', str(e)
