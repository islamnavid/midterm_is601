
"""Manage calculator history."""

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
