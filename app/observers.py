
"""Observers for calculator events."""

from pathlib import Path

from app.logger import Logger


class LoggingObserver:
    """Log calculator events and completed calculations."""

    def __init__(self, log_file="calculator.log"):
        self.logger = Logger.create_logger(log_file)

    def update(self, calculation):
        """Record a completed calculation."""
        self.logger.info(
            "%s: %s, %s = %s",
            calculation.operation,
            calculation.operand1,
            calculation.operand2,
            calculation.result,
        )

    def log_warning(self, message):
        """Record a calculator warning."""
        self.logger.warning("%s", message)

    def log_error(self, message):
        """Record a calculator error."""
        self.logger.error("%s", message)


class AutoSaveObserver:
    """Automatically save calculation history to CSV."""

    def __init__(
        self,
        history,
        file_path="calculation_history.csv"
    ):
        self.history = history
        self.file_path = Path(file_path)

    def update(self, calculation):
        """Save the updated calculation history."""
        self.history.save_to_csv(self.file_path)
