import logging
import sys
from backend.config import settings


def get_logger(name: str = "career_ai") -> logging.Logger:
    """
    Get a configured logger instance for Enterprise AI platform modules.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = get_logger("career_ai")
