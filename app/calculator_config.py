
"""Configuration management for the calculator application."""

import codecs
import math
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class CalculatorConfig:
    """Load and validate calculator settings from environment variables."""

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

        auto_save_value = os.getenv(
            "CALCULATOR_AUTO_SAVE", "true"
        ).strip().lower()

        if auto_save_value not in ("true", "false"):
            raise ValueError(
                "CALCULATOR_AUTO_SAVE must be true or false."
            )

        self.auto_save = auto_save_value == "true"

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
        """Validate configuration values before starting the calculator."""
        if self.max_history_size <= 0:
            raise ValueError(
                "Maximum history size must be positive."
            )

        if self.precision < 0:
            raise ValueError(
                "Precision cannot be negative."
            )

        if not math.isfinite(self.max_input_value):
            raise ValueError(
                "Maximum input value must be finite."
            )

        if self.max_input_value <= 0:
            raise ValueError(
                "Maximum input value must be positive."
            )

        try:
            codecs.lookup(self.default_encoding)
        except LookupError as error:
            raise ValueError(
                f"Unsupported encoding: {self.default_encoding}"
            ) from error
