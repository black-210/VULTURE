"""Exception Handling and Recovery

Robust error handling with recovery strategies.
"""

from typing import Callable, Optional, Any
import logging
import time


class ErrorRecovery:
    """Error recovery strategy"""
    
    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.logger = logging.getLogger("vulture.errors")
    
    def retry(self, func: Callable, *args, **kwargs) -> Any:
        """Retry function with exponential backoff"""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    self.logger.error(f"Failed after {self.max_retries} attempts: {e}")
                    raise
                
                wait_time = self.backoff_factor * (2 ** attempt)
                self.logger.warning(
                    f"Attempt {attempt + 1} failed: {e}. "
                    f"Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)


class ErrorHandler:
    """Error handling system"""
    
    def __init__(self):
        self.logger = logging.getLogger("vulture.error_handler")
        self.recovery = ErrorRecovery()
    
    def handle_exception(self, exc: Exception, context: str = "") -> None:
        """Handle exception with logging"""
        self.logger.error(
            f"Exception in {context}: {type(exc).__name__}: {exc}",
            exc_info=True
        )
    
    def safe_execute(
        self,
        func: Callable,
        *args,
        fallback: Optional[Any] = None,
        **kwargs
    ) -> Any:
        """Execute function safely with fallback"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.handle_exception(e, func.__name__)
            return fallback
    
    def retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """Execute with retry and backoff"""
        return self.recovery.retry(func, *args, **kwargs)
