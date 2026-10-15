"""Main calculator class."""

from app.calculation import Calculation
from app.history import CalculationHistory


class Calculator:
    """Manage calculations and calculation history."""

    def __init__(self):
        self.history = CalculationHistory()
        self.observers = []

    def add_observer(self, observer):
        """Register an observer."""
        self.observers.append(observer)

    def notify_observers(self, calculation):
        """Notify observers when a calculation is performed."""
        for observer in self.observers:
            observer.update(calculation)

    def calculate(self, operation, operand1, operand2):
        """Perform a calculation and store its result."""
        calculation = Calculation(operation, operand1, operand2)

        self.history.add(calculation)
        self.notify_observers(calculation)

        return calculation.result