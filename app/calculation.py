
"""Represent individual calculator calculations."""

from dataclasses import dataclass, field
from datetime import datetime

from app.operations import OperationFactory


@dataclass
class Calculation:
    """Store an arithmetic calculation and its result."""

    operation: str
    operand1: float
    operand2: float
    result: float = field(init=False)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Calculate the result after initialization."""
        operation_function = OperationFactory.create_operation(
            self.operation
        )
        self.result = operation_function(
            self.operand1, self.operand2
        )

    def to_dict(self):
        """Convert the calculation to a dictionary."""
        return {
            "operation": self.operation,
            "operand1": self.operand1,
            "operand2": self.operand2,
            "result": self.result,
            "timestamp": self.timestamp.isoformat(),
        }
