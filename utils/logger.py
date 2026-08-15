# utils/logger.py
"""Simple logging utility for the Voice-Notes app."""
import logging
import sys
from typing import Optional

_logger: Optional[logging.Logger] = None


def get_logger(name: str = "voice_notes") -> logging.Logger:
    """Return a configured logger.

    Logs to STDOUT with a clean format at INFO level.
    """
    global _logger
    if _logger is not None:
        return _logger

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-5s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    _logger = logger
    return logger
