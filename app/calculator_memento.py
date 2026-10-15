
"""Memento pattern for saving calculator history snapshots."""

from copy import deepcopy


class CalculatorMemento:
    """Store a snapshot of calculation history."""

    def __init__(self, history):
        self._history = deepcopy(history)

    def get_state(self):
        """Return an independent copy of the saved history."""
        return deepcopy(self._history)
