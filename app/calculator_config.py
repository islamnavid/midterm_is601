"""Configuration management for the calculator application."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class CalculatorConfig:
    """Manage calculator configuration using environment variables."""

    def __init__(self):
        self.log_dir = Path(
            os.getenv("CALCULATOR_LOG_DIR", "logs")
        )
        self.history_dir = Path(
            os.getenv("CALCULATOR_HISTORY_DIR", "history")
        )

        self.max_history_size = int(
            os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100")
        )
        self.auto_save = os.getenv(
            "CALCULATOR_AUTO_SAVE", "true"
        ).lower() == "true"

        self.precision = int(
            os.getenv("CALCULATOR_PRECISION", "2")
        )
        self.max_input_value = float(
            os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000")
        )
        self.default_encoding = os.getenv(
            "CALCULATOR_DEFAULT_ENCODING", "utf-8"
        )

        self.log_file = self.log_dir / os.getenv(
            "CALCULATOR_LOG_FILE", "calculator.log"
        )
        self.history_file = self.history_dir / os.getenv(
            "CALCULATOR_HISTORY_FILE", "calculation_history.csv"
        )

        self.validate()

        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def validate(self):
        """Validate configuration values."""
        if self.max_history_size <= 0:
            raise ValueError("Maximum history size must be positive.")

        if self.precision < 0:
            raise ValueError("Precision cannot be negative.")

        if self.max_input_value <= 0:
            raise ValueError("Maximum input value must be positive.")