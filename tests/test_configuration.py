
"""Tests for calculator configuration and precision."""

import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.history import CalculationHistory
from app.calculation import Calculation


def test_default_configuration(monkeypatch):
    """Verify default configuration values."""
    monkeypatch.delenv("CALCULATOR_PRECISION", raising=False)
    monkeypatch.delenv(
        "CALCULATOR_MAX_HISTORY_SIZE", raising=False
    )

    config = CalculatorConfig()

    assert config.precision == 2
    assert config.max_history_size == 100


def test_custom_precision(monkeypatch):
    """Verify custom precision from environment."""
    monkeypatch.setenv("CALCULATOR_PRECISION", "4")

    calculator = Calculator()

    assert calculator.config.precision == 4
    assert calculator.format_result(10 / 3) == "3.3333"


def test_default_precision():
    """Verify two-decimal formatting."""
    calculator = Calculator()

    assert calculator.format_result(15.0) == "15.00"
    assert calculator.format_result(7.5) == "7.50"


def test_custom_history_limit(monkeypatch):
    """Verify history limit from environment."""
    monkeypatch.setenv(
        "CALCULATOR_MAX_HISTORY_SIZE", "3"
    )

    calculator = Calculator()

    for number in range(5):
        calculator.calculate("add", number, 1)

    assert calculator.history.count() == 3
    assert calculator.history.get_all()[0].operand1 == 2


def test_invalid_history_limit():
    """Reject a nonpositive history limit."""
    with pytest.raises(ValueError):
        CalculationHistory(max_history_size=0)


def test_invalid_precision(monkeypatch):
    """Reject negative precision."""
    monkeypatch.setenv("CALCULATOR_PRECISION", "-1")

    with pytest.raises(ValueError):
        CalculatorConfig()


def test_history_limit_directly():
    """Verify CalculationHistory removes oldest entries."""
    history = CalculationHistory(max_history_size=2)

    history.add(Calculation("add", 1, 1))
    history.add(Calculation("add", 2, 2))
    history.add(Calculation("add", 3, 3))

    assert history.count() == 2
    assert history.get_all()[0].operand1 == 2


def test_undo_after_loading(tmp_path):
    """Verify loading CSV history can be undone."""
    history = CalculationHistory()

    history.add(Calculation("add", 10, 5))

    csv_path = tmp_path / "history.csv"
    history.save_to_csv(csv_path)

    history.clear()
    history.load_from_csv(csv_path)

    assert history.count() == 1
    assert history.undo() is True
    assert history.count() == 0


@pytest.mark.parametrize(
    "value",
    ["true", "TRUE", "True", " true "],
)
def test_auto_save_enabled(monkeypatch, value):
    """Accept valid true values for automatic saving."""
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", value)

    config = CalculatorConfig()

    assert config.auto_save is True


@pytest.mark.parametrize(
    "value",
    ["false", "FALSE", "False", " false "],
)
def test_auto_save_disabled(monkeypatch, value):
    """Accept valid false values for automatic saving."""
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", value)

    config = CalculatorConfig()

    assert config.auto_save is False


@pytest.mark.parametrize(
    "value",
    ["maybe", "yes", "1", ""],
)
def test_invalid_auto_save(monkeypatch, value):
    """Reject invalid automatic saving settings."""
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", value)

    with pytest.raises(
        ValueError,
        match="CALCULATOR_AUTO_SAVE must be true or false"
    ):
        CalculatorConfig()


@pytest.mark.parametrize(
    "value",
    ["0", "-1", "nan", "inf", "-inf"],
)
def test_invalid_max_input_value(monkeypatch, value):
    """Reject invalid maximum input values."""
    monkeypatch.setenv(
        "CALCULATOR_MAX_INPUT_VALUE", value
    )

    with pytest.raises(ValueError):
        CalculatorConfig()


def test_invalid_encoding(monkeypatch):
    """Reject unsupported text encodings."""
    monkeypatch.setenv(
        "CALCULATOR_DEFAULT_ENCODING",
        "not-a-real-encoding"
    )

    with pytest.raises(
        ValueError,
        match="Unsupported encoding"
    ):
        CalculatorConfig()


def test_valid_custom_encoding(monkeypatch):
    """Accept a valid text encoding."""
    monkeypatch.setenv(
        "CALCULATOR_DEFAULT_ENCODING", "utf-8"
    )

    config = CalculatorConfig()

    assert config.default_encoding == "utf-8"


def test_invalid_environment_history_limit(monkeypatch):
    """Reject invalid history limits from environment."""
    monkeypatch.setenv(
        "CALCULATOR_MAX_HISTORY_SIZE", "0"
    )

    with pytest.raises(
        ValueError,
        match="Maximum history size must be positive"
    ):
        CalculatorConfig()
