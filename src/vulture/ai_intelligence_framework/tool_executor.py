"""Tool executor for sandboxed execution."""
import subprocess
import logging
logger = logging.getLogger(__name__)
class ToolExecutor:
    def __init__(self, sandbox=True):
        self.sandbox = sandbox
    def execute_python(self, code, timeout=30):
        if not self.sandbox:
            try:
                return eval(code)
            except Exception as e:
                logger.error(f"Execution error: {e}")
                return None
        try:
            result = subprocess.run(['python', '-c', code], capture_output=True, timeout=timeout, text=True)
            return result.stdout
        except subprocess.TimeoutExpired:
            logger.error("Execution timeout")
            return None
    def execute_command(self, command, timeout=30):
        try:
            result = subprocess.run(command.split(), capture_output=True, timeout=timeout, text=True)
            return result.stdout
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return None