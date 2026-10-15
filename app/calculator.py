
"""Main calculator class."""

from app.calculation import Calculation
from app.history import CalculationHistory
from app.calculator_config import CalculatorConfig
from app.input_validators import validate_number


class Calculator:
    """Manage calculations and calculation history."""

    def __init__(self):
        """Initialize calculator with configuration and history."""

        # Load configuration from environment variables.
        self.config = CalculatorConfig()

        # Initialize history with the configured maximum size.
        self.history = CalculationHistory(
            max_history_size=self.config.max_history_size
        )

        # Store registered observers.
        self.observers = []

    def add_observer(self, observer):
        """Register an observer."""
        self.observers.append(observer)

    def notify_observers(self, calculation):
        """Notify observers when a calculation is performed."""
        for observer in self.observers:
            observer.update(calculation)

    def calculate(self, operation, operand1, operand2):
        """Validate inputs, perform calculation, and save result."""

        # Validate both operands against the configured input limit.
        operand1 = validate_number(
            operand1,
            self.config.max_input_value
        )

        operand2 = validate_number(
            operand2,
            self.config.max_input_value
        )

        # Create and execute the calculation.
        # Invalid calculations should not modify history.
        calculation = Calculation(
            operation,
            operand1,
            operand2
        )

        # Save history state before adding a successful calculation.
        self.history.checkpoint()

        # Add the calculation to history.
        self.history.add(calculation)

        # Notify registered observers.
        self.notify_observers(calculation)

        return calculation.result

    def format_result(self, result):
        """Format a calculation result using configured precision."""
        return f"{result:.{self.config.precision}f}"
