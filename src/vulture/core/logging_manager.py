"""Centralized Logging Management

Configurable logging with rotation and levels.
"""

import logging
import logging.handlers
from typing import Optional
from pathlib import Path


class Logger:
    """Logger wrapper"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def debug(self, msg: str) -> None:
        self.logger.debug(msg)
    
    def info(self, msg: str) -> None:
        self.logger.info(msg)
    
    def warning(self, msg: str) -> None:
        self.logger.warning(msg)
    
    def error(self, msg: str) -> None:
        self.logger.error(msg)
    
    def critical(self, msg: str) -> None:
        self.logger.critical(msg)


class LoggingManager:
    """Logging configuration manager"""
    
    def __init__(self):
        self.loggers: dict = {}
    
    def configure_root_logger(
        self,
        level: int = logging.INFO,
        log_file: Optional[str] = None,
        max_bytes: int = 10485760,
        backup_count: int = 5
    ) -> None:
        """Configure root logger"""
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # File handler with rotation
        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
    
    def get_logger(self, name: str) -> Logger:
        """Get or create logger"""
        if name not in self.loggers:
            self.loggers[name] = Logger(name)
        return self.loggers[name]
