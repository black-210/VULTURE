"""Sandboxed Python/command execution with timeout."""

import subprocess
import logging
from typing import Dict, Any
import tempfile
from pathlib import Path
import time

logger = logging.getLogger(__name__)


class ToolExecutor:
    """Safe sandboxed code execution."""

    def __init__(self, timeout: int = 30, sandbox: bool = True):
        """
        Args:
            timeout: Execution timeout (seconds)
            sandbox: Use subprocess sandboxing
        """
        self.timeout = timeout
        self.sandbox = sandbox

    def execute_python(self, code: str, globals_dict: Dict = None) -> Dict[str, Any]:
        """Execute Python code.
        
        Args:
            code: Python code string
            globals_dict: Global variables
            
        Returns:
            Execution result dict
        """
        if not self.sandbox:
            # Direct execution (NOT RECOMMENDED)
            try:
                exec_globals = globals_dict or {}
                exec(code, exec_globals)
                return {'success': True, 'output': str(exec_globals)}
            except Exception as e:
                return {'success': False, 'error': str(e)}
        
        # Sandboxed via subprocess
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            script_path = f.name
        
        try:
            result = subprocess.run(
                ['python', script_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': f'Timeout after {self.timeout}s'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            Path(script_path).unlink()

    def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute shell command.
        
        Args:
            command: Shell command
            
        Returns:
            Execution result dict
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': f'Command timeout after {self.timeout}s'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
