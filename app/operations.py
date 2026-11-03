
"""Arithmetic operations for the calculator application."""

import math


def check_result(result):
    """Reject results that are infinite or not a real number."""
    if isinstance(result, complex):
        raise ValueError("Result cannot be a complex number.")

    try:
        if not math.isfinite(result):
            raise ValueError("Calculation result is not finite.")
    except OverflowError as error:
        raise ValueError("Calculation result is too large.") from error

    return result


def validate_inputs(a, b):
    """Ensure both inputs are finite numbers."""
    for value in (a, b):
        if isinstance(value, (bool, complex)) or not isinstance(
            value, (int, float)
        ):
            raise ValueError("Both inputs must be real numbers.")

        if not math.isfinite(value):
            raise ValueError("Inputs must be finite numbers.")


def safe_operation(operation):
    """Validate inputs and handle arithmetic overflow."""
    def wrapper(a, b):
        validate_inputs(a, b)
        try:
            result = operation(a, b)
            return check_result(result)
        except (OverflowError, ZeroDivisionError) as error:
            raise ValueError(
                "Calculation failed due to overflow or division by zero."
            ) from error

    return wrapper


@safe_operation
def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


@safe_operation
def subtract(a: float, b: float) -> float:
    """Return the difference between two numbers."""
    return a - b


@safe_operation
def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


@safe_operation
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


@safe_operation
def power(a: float, b: float) -> float:
    """Raise a number to a power."""
    if a == 0 and b < 0:
        raise ValueError("Zero cannot have a negative exponent.")
    return a ** b


@safe_operation
def root(a: float, b: float) -> float:
    """Calculate the nth root of a number."""
    if b == 0:
        raise ValueError("Root degree cannot be zero.")

    if a == 0 and b < 0:
        raise ValueError("Cannot calculate a negative root of zero.")

    if a < 0:
        if not float(b).is_integer() or int(b) % 2 == 0:
            raise ValueError(
                "Negative numbers require an odd integer root."
            )
        return -((-a) ** (1 / b))

    return a ** (1 / b)


@safe_operation
def modulus(a: float, b: float) -> float:
    """Return the remainder of division."""
    if b == 0:
        raise ValueError("Cannot calculate modulus with zero.")
    return a % b


@safe_operation
def int_divide(a: float, b: float) -> float:
    """Perform integer division."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a // b


@safe_operation
def percent(a: float, b: float) -> float:
    """Calculate a as a percentage of b."""
    if b == 0:
        raise ValueError("Cannot calculate percentage with zero.")
    return (a / b) * 100


@safe_operation
def abs_diff(a: float, b: float) -> float:
    """Return the absolute difference between two numbers."""
    return abs(a - b)


class OperationFactory:
    """Factory for selecting calculator operations."""

    _operations = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
        "power": power,
        "root": root,
        "modulus": modulus,
        "int_divide": int_divide,
        "percent": percent,
        "abs_diff": abs_diff,
    }

    @classmethod
    def create_operation(cls, operation_name: str):
        """Return the operation matching the given name."""
        operation = cls._operations.get(operation_name.lower())

        if operation is None:
            raise ValueError(
                f"Unsupported operation: {operation_name}"
            )

        return operation

    @classmethod
    def list_operations(cls):
        """Return all available arithmetic operation names."""
        return list(cls._operations.keys())
