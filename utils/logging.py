"""Logging setup for TERFALCOM."""
import logging
from typing import Optional
from pathlib import Path


def setup_logger(
    name: str,
    level: str = 'INFO',
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Setup a logger instance.
    
    Args:
        name: Logger name.
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Optional file to write logs to.
    
    Returns:
        Configured logger instance.
    
    Raises:
        ValueError: If level is invalid
    """
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if level.upper() not in valid_levels:
        raise ValueError(f"Invalid log level: {level}. Must be one of {valid_levels}")

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Prevent duplicate handlers across repeated setup calls.
    logger.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (OSError, IOError) as exc:
            logger.warning(f"Could not create log file {log_file}: {exc}")

    return logger
