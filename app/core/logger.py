import logging
import sys
from logging.handlers import RotatingFileHandler
from app.config import settings


def setup_logger(name: str = "HALAS") -> logging.Logger:
    """
    Create and configure structured logger for HALAS system.
    """

    logger = logging.getLogger(name)
    logger.setLevel(settings.logging.log_level)

    if logger.hasHandlers():
        return logger  

    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating File Handler (auto-rotates logs)
    file_handler = RotatingFileHandler(
        settings.logging.log_file,
        maxBytes=5 * 1024 * 1024,  
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Global logger instance
logger = setup_logger()