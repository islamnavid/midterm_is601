
"""Manage calculator history."""
from pathlib import Path
import pandas as pd
from app.calculation import Calculation


class CalculationHistory:
    """Store and manage completed calculations."""

    def __init__(self):
        self._history = []

    def add(self, calculation: Calculation):
        """Add a calculation to history."""
        self._history.append(calculation)

    def get_all(self):
        """Return all stored calculations."""
        return self._history.copy()

    def get_last(self):
        """Return the most recent calculation."""
        if not self._history:
            return None
        return self._history[-1]

    def clear(self):
        """Remove all calculations from history."""
        self._history.clear()

    def count(self):
        """Return the number of stored calculations."""
        return len(self._history)

    def save_to_csv(self, file_path):
        """Save calculation history to a CSV file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        columns = [
            "operation",
            "operand1",
            "operand2",
            "result",
            "timestamp",
        ]

        records = [
            calculation.to_dict()
            for calculation in self._history
        ]

        dataframe = pd.DataFrame(records, columns=columns)
        dataframe.to_csv(path, index=False)

    def load_from_csv(self, file_path):
        """Load calculation history from a CSV file."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"History file not found: {path}"
            )

        dataframe = pd.read_csv(path)
        required_columns = {
            "operation",
            "operand1",
            "operand2",
            "result",
            "timestamp",
        }

        if not required_columns.issubset(dataframe.columns):
            raise ValueError("Invalid history CSV format")

        loaded_calculations = []

        for _, row in dataframe.iterrows():
            calculation = Calculation(
                operation=str(row["operation"]),
                operand1=float(row["operand1"]),
                operand2=float(row["operand2"]),
            )
            calculation.timestamp = pd.to_datetime(
                row["timestamp"]
            ).to_pydatetime()
            loaded_calculations.append(calculation)

        self._history = loaded_calculations
