"""
VULTURE Advanced Error Handler Module
======================================
Sophisticated error handling with automatic recovery, detailed logging,
error categorization, and intelligent retry mechanisms.

Features:
    - Automatic error recovery
    - Error categorization and classification
    - Detailed error context preservation
    - Smart retry strategies
    - Error aggregation and reporting
    - Error hooks for custom handling
"""

import logging
import traceback
import functools
from typing import Any, Callable, Dict, List, Optional, Type, Tuple
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    FATAL = "fatal"


class ErrorCategory(Enum):
    """Error categories"""
    VALIDATION = "validation"
    NETWORK = "network"
    RESOURCE = "resource"
    PERMISSION = "permission"
    CONFIGURATION = "configuration"
    RUNTIME = "runtime"
    UNKNOWN = "unknown"


@dataclass
class ErrorContext:
    """Comprehensive error context"""
    error_type: Type[Exception]
    message: str
    severity: ErrorSeverity
    category: ErrorCategory
    timestamp: datetime = field(default_factory=datetime.now)
    traceback_str: str = ""
    context_data: Dict[str, Any] = field(default_factory=dict)
    recovery_attempted: bool = False
    recovery_success: bool = False
    recovery_strategy: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'error_type': self.error_type.__name__,
            'message': self.message,
            'severity': self.severity.value,
            'category': self.category.value,
            'timestamp': self.timestamp.isoformat(),
            'recovery_attempted': self.recovery_attempted,
            'recovery_success': self.recovery_success,
            'recovery_strategy': self.recovery_strategy,
            'context_data': self.context_data
        }


class ErrorCategorizer:
    """Categorize errors automatically"""
    
    CATEGORY_MAPPING = {
        # Validation errors
        ValueError: ErrorCategory.VALIDATION,
        TypeError: ErrorCategory.VALIDATION,
        KeyError: ErrorCategory.VALIDATION,
        
        # Network errors
        ConnectionError: ErrorCategory.NETWORK,
        TimeoutError: ErrorCategory.NETWORK,
        OSError: ErrorCategory.NETWORK,
        
        # Resource errors
        MemoryError: ErrorCategory.RESOURCE,
        FileNotFoundError: ErrorCategory.RESOURCE,
        IOError: ErrorCategory.RESOURCE,
        
        # Permission errors
        PermissionError: ErrorCategory.PERMISSION,
        
        # Configuration errors
        RuntimeError: ErrorCategory.RUNTIME,
    }
    
    @classmethod
    def categorize(cls, error: Exception) -> ErrorCategory:
        """Categorize an exception"""
        error_type = type(error)
        
        for exc_class, category in cls.CATEGORY_MAPPING.items():
            if isinstance(error, exc_class):
                return category
        
        return ErrorCategory.UNKNOWN
    
    @classmethod
    def get_severity(cls, category: ErrorCategory) -> ErrorSeverity:
        """Determine severity from category"""
        severity_map = {
            ErrorCategory.VALIDATION: ErrorSeverity.WARNING,
            ErrorCategory.NETWORK: ErrorSeverity.ERROR,
            ErrorCategory.RESOURCE: ErrorSeverity.CRITICAL,
            ErrorCategory.PERMISSION: ErrorSeverity.ERROR,
            ErrorCategory.CONFIGURATION: ErrorSeverity.WARNING,
            ErrorCategory.RUNTIME: ErrorSeverity.ERROR,
            ErrorCategory.UNKNOWN: ErrorSeverity.ERROR,
        }
        return severity_map.get(category, ErrorSeverity.ERROR)


class RecoveryStrategy:
    """Error recovery strategies"""
    
    @staticmethod
    def retry(func: Callable, args: tuple, kwargs: dict, max_attempts: int = 3,
              backoff_factor: float = 2.0) -> Any:
        """Retry strategy with exponential backoff"""
        import time
        
        last_error = None
        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < max_attempts - 1:
                    wait_time = (backoff_factor ** attempt)
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed, "
                        f"retrying in {wait_time}s"
                    )
                    time.sleep(wait_time)
        
        raise last_error
    
    @staticmethod
    def fallback(primary_func: Callable, fallback_func: Callable,
                 args: tuple, kwargs: dict) -> Any:
        """Fallback strategy"""
        try:
            return primary_func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Primary function failed, using fallback: {e}")
            try:
                return fallback_func(*args, **kwargs)
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
                raise
    
    @staticmethod
    def default_value(func: Callable, default: Any, args: tuple, kwargs: dict) -> Any:
        """Return default value on error"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Function failed, returning default value: {e}")
            return default
    
    @staticmethod
    def cleanup_and_retry(func: Callable, cleanup_func: Callable,
                         args: tuple, kwargs: dict) -> Any:
        """Cleanup resources and retry"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.info("Performing cleanup before retry...")
            try:
                cleanup_func()
                return func(*args, **kwargs)
            except Exception as retry_error:
                logger.error(f"Cleanup and retry failed: {retry_error}")
                raise


class ErrorAggregator:
    """Aggregate and track multiple errors"""
    
    def __init__(self, max_errors: int = 1000):
        self.errors: List[ErrorContext] = []
        self.max_errors = max_errors
    
    def add_error(self, context: ErrorContext) -> None:
        """Add error to aggregator"""
        self.errors.append(context)
        
        if len(self.errors) > self.max_errors:
            self.errors.pop(0)
    
    def get_errors_by_category(self, category: ErrorCategory) -> List[ErrorContext]:
        """Get errors by category"""
        return [e for e in self.errors if e.category == category]
    
    def get_errors_by_severity(self, severity: ErrorSeverity) -> List[ErrorContext]:
        """Get errors by severity"""
        return [e for e in self.errors if e.severity == severity]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get error summary"""
        total = len(self.errors)
        by_category = {}
        by_severity = {}
        
        for error in self.errors:
            cat = error.category.value
            sev = error.severity.value
            
            by_category[cat] = by_category.get(cat, 0) + 1
            by_severity[sev] = by_severity.get(sev, 0) + 1
        
        return {
            'total_errors': total,
            'by_category': by_category,
            'by_severity': by_severity,
            'recovery_success_rate': self._get_recovery_rate()
        }
    
    def _get_recovery_rate(self) -> float:
        """Get error recovery success rate"""
        attempted = [e for e in self.errors if e.recovery_attempted]
        if not attempted:
            return 0.0
        
        successful = [e for e in attempted if e.recovery_success]
        return len(successful) / len(attempted) * 100
    
    def export_report(self, filepath: Path) -> None:
        """Export error report to JSON"""
        report = {
            'summary': self.get_summary(),
            'errors': [e.to_dict() for e in self.errors],
            'exported_at': datetime.now().isoformat()
        }
        
        filepath.write_text(json.dumps(report, indent=2))
        logger.info(f"Error report exported to {filepath}")
    
    def clear(self) -> None:
        """Clear error history"""
        self.errors.clear()


class AdvancedErrorHandler:
    """Central error handling orchestrator"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if self.initialized:
            return
        
        self.aggregator = ErrorAggregator()
        self.error_hooks: List[Callable] = []
        self.initialized = True
    
    def register_hook(self, hook: Callable) -> None:
        """Register error hook for custom handling"""
        self.error_hooks.append(hook)
    
    def handle_error(self, error: Exception, context_data: Optional[Dict] = None,
                    recovery_strategy: Optional[Callable] = None) -> ErrorContext:
        """Handle error with full context"""
        category = ErrorCategorizer.categorize(error)
        severity = ErrorCategorizer.get_severity(category)
        
        error_context = ErrorContext(
            error_type=type(error),
            message=str(error),
            severity=severity,
            category=category,
            traceback_str=traceback.format_exc(),
            context_data=context_data or {}
        )
        
        # Attempt recovery if strategy provided
        if recovery_strategy:
            try:
                recovery_strategy()
                error_context.recovery_attempted = True
                error_context.recovery_success = True
                error_context.recovery_strategy = recovery_strategy.__name__
            except Exception as recovery_error:
                logger.error(f"Recovery failed: {recovery_error}")
                error_context.recovery_attempted = True
                error_context.recovery_success = False
        
        # Add to aggregator
        self.aggregator.add_error(error_context)
        
        # Call hooks
        for hook in self.error_hooks:
            try:
                hook(error_context)
            except Exception as hook_error:
                logger.error(f"Error hook failed: {hook_error}")
        
        # Log the error
        log_level = {
            ErrorSeverity.INFO: logging.INFO,
            ErrorSeverity.WARNING: logging.WARNING,
            ErrorSeverity.ERROR: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL,
            ErrorSeverity.FATAL: logging.CRITICAL,
        }[severity]
        
        logger.log(
            log_level,
            f"[{category.value.upper()}] {error}\n{error_context.traceback_str}"
        )
        
        return error_context
    
    def retry_with_backoff(self, func: Callable, *args,
                          max_attempts: int = 3, backoff_factor: float = 2.0, **kwargs) -> Any:
        """Retry function with exponential backoff"""
        return RecoveryStrategy.retry(func, args, kwargs, max_attempts, backoff_factor)
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary"""
        return self.aggregator.get_summary()
    
    def export_error_report(self, filepath: Path) -> None:
        """Export error report"""
        self.aggregator.export_report(filepath)


def handle_errors(recovery_strategy: Optional[Callable] = None):
    """Decorator for automatic error handling"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler = AdvancedErrorHandler()
                handler.handle_error(e, recovery_strategy=recovery_strategy)
                raise
        return wrapper
    return decorator


# Global instance
_error_handler = AdvancedErrorHandler()


def get_error_handler() -> AdvancedErrorHandler:
    """Get global error handler"""
    return _error_handler
