"""Input validation utilities for the calculator."""

import math

from app.exceptions import ValidationError


def validate_number(value, max_value):
    """Validate a numeric operand against the configured limit."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError("Input must be a number.")

    if not math.isfinite(value):
        raise ValidationError("Input must be a finite number.")

    if abs(value) > max_value:
        raise ValidationError(
            f"Input must be between {-max_value:g} and {max_value:g}."
        )

    return value