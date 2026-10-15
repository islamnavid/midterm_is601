
"""Manage calculator history."""

from pathlib import Path

import pandas as pd

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


class CalculationHistory:
    """Store and manage completed calculations."""

    def __init__(self, max_history_size=100):
        if max_history_size <= 0:
            raise ValueError(
                "Maximum history size must be positive."
            )

        self.max_history_size = max_history_size
        self._history = []
        self._undo_stack = []
        self._redo_stack = []

    def save_state(self) -> CalculatorMemento:
        """Create a snapshot of the current history."""
        return CalculatorMemento(self._history)

    def restore_state(self, memento: CalculatorMemento):
        """Restore history from a saved snapshot."""
        self._history = memento.get_state()

    def checkpoint(self):
        """Save the current state for undo."""
        self._undo_stack.append(self.save_state())
        self._redo_stack.clear()

    def undo(self):
        """Restore the previous saved state."""
        if not self._undo_stack:
            return False

        self._redo_stack.append(self.save_state())
        self.restore_state(self._undo_stack.pop())
        return True

    def redo(self):
        """Restore a previously undone state."""
        if not self._redo_stack:
            return False

        self._undo_stack.append(self.save_state())
        self.restore_state(self._redo_stack.pop())
        return True

    def add(self, calculation: Calculation):
        """Add a calculation and enforce history size."""
        self._history.append(calculation)

        if len(self._history) > self.max_history_size:
            self._history.pop(0)

    def get_all(self):
        """Return all stored calculations."""
        return self._history.copy()

    def get_last(self):
        """Return the most recent calculation."""
        if not self._history:
            return None

        return self._history[-1]

    def clear(self):
        """Clear history while preserving undo support."""
        self.checkpoint()
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

        dataframe = pd.DataFrame(
            records,
            columns=columns
        )

        dataframe.to_csv(path, index=False)

    def load_from_csv(self, file_path):
        """Load history from CSV with undo support."""
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
            raise ValueError(
                "Invalid history CSV format"
            )

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

        # Preserve the previous state for undo.
        self.checkpoint()

        # Keep only the most recent calculations.
        self._history = loaded_calculations[
            -self.max_history_size:
        ]
