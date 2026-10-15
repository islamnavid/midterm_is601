
"""Centralized logging configuration for the calculator."""

import logging
from pathlib import Path
from uuid import uuid4


class Logger:
    """Create configured file loggers for calculator components."""

    @staticmethod
    def create_logger(log_file="calculator.log"):
        """Create a unique logger that writes to the specified file."""
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(
            f"calculator.observer.{uuid4().hex}"
        )

        logger.setLevel(logging.INFO)
        logger.propagate = False

        handler = logging.FileHandler(
            log_path,
            encoding="utf-8"
        )

        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
        )

        logger.addHandler(handler)

        return logger
