"""Observers for calculator events."""

import logging


class LoggingObserver:
    """Log completed calculations."""

    def __init__(self, log_file="calculator.log"):
        self.logger = logging.getLogger(
            f"calculator.observer.{id(self)}"
        )
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        handler = logging.FileHandler(log_file)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
        )
        self.logger.addHandler(handler)

    def update(self, calculation):
        """Record a completed calculation."""
        self.logger.info(
            "%s: %s, %s = %s",
            calculation.operation,
            calculation.operand1,
            calculation.operand2,
            calculation.result,
        )

class AutoSaveObserver:
    """Automatically save calculation history to CSV."""

    def __init__(self, history, file_path="calculation_history.csv"):
        self.history = history
        self.file_path = file_path

    def update(self, calculation):
        """Save the updated calculation history."""
        self.history.save_to_csv(self.file_path)