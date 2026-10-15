
"""Arithmetic operations for the calculator application."""


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference between two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide two numbers, checking for division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def power(a: float, b: float) -> float:
    """Raise a number to a power."""
    result = a ** b
    if isinstance(result, complex):
        raise ValueError("Result cannot be a complex number.")
    return result


def root(a: float, b: float) -> float:
    """Calculate the nth root of a number."""
    if b == 0:
        raise ValueError("Root degree cannot be zero.")
    if a < 0:
        if not b.is_integer() or int(b) % 2 == 0:
            raise ValueError("Negative numbers require an odd integer root.")
        return -((-a) ** (1 / b))
    return a ** (1 / b)


def modulus(a: float, b: float) -> float:
    """Return the remainder of division."""
    if b == 0:
        raise ValueError("Cannot calculate modulus with zero.")
    return a % b


def int_divide(a: float, b: float) -> float:
    """Perform integer division."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a // b


def percent(a: float, b: float) -> float:
    """Calculate a as a percentage of b."""
    if b == 0:
        raise ValueError("Cannot calculate percentage with zero.")
    return (a / b) * 100


def abs_diff(a: float, b: float) -> float:
    """Return the absolute difference between two numbers."""
    return abs(a - b)
