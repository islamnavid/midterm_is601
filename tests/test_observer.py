
"""Tests for calculator observers and logging."""

import logging

import pandas as pd

from app.calculator import Calculator
from app.observers import AutoSaveObserver, LoggingObserver


def test_auto_save_observer(tmp_path):
    """Test automatic saving of calculation history."""
    file_path = tmp_path / "calculation_history.csv"

    calculator = Calculator()
    observer = AutoSaveObserver(
        calculator.history,
        file_path=str(file_path)
    )
    calculator.add_observer(observer)

    calculator.calculate("add", 10, 5)
    calculator.calculate("multiply", 4, 5)

    assert file_path.exists()

    data = pd.read_csv(file_path)

    assert len(data) == 2
    assert data["result"].tolist() == [15, 20]
    assert data["operation"].tolist() == [
        "add",
        "multiply",
    ]


def test_logging_observer_info(tmp_path):
    """Test that successful calculations are logged."""
    log_file = tmp_path / "calculator.log"

    calculator = Calculator()
    observer = LoggingObserver(log_file=log_file)

    calculator.add_observer(observer)
    calculator.calculate("add", 10, 5)

    for handler in observer.logger.handlers:
        handler.flush()

    assert log_file.exists()

    log_content = log_file.read_text(encoding="utf-8")

    assert "INFO" in log_content
    assert "add: 10, 5 = 15" in log_content


def test_logging_observer_warning(tmp_path):
    """Test warning-level logging."""
    log_file = tmp_path / "calculator.log"

    observer = LoggingObserver(log_file=log_file)

    observer.log_warning("Invalid calculator input")

    for handler in observer.logger.handlers:
        handler.flush()

    log_content = log_file.read_text(encoding="utf-8")

    assert "WARNING" in log_content
    assert "Invalid calculator input" in log_content


def test_logging_observer_error(tmp_path):
    """Test error-level logging."""
    log_file = tmp_path / "calculator.log"

    observer = LoggingObserver(log_file=log_file)

    observer.log_error("Division by zero")

    for handler in observer.logger.handlers:
        handler.flush()

    log_content = log_file.read_text(encoding="utf-8")

    assert "ERROR" in log_content
    assert "Division by zero" in log_content


def test_logging_observer_log_levels(tmp_path):
    """Test that all three logging levels are recorded."""
    log_file = tmp_path / "calculator.log"

    observer = LoggingObserver(log_file=log_file)

    calculator = Calculator()
    calculator.add_observer(observer)

    calculator.calculate("multiply", 4, 5)
    observer.log_warning("Test warning")
    observer.log_error("Test error")

    for handler in observer.logger.handlers:
        handler.flush()

    log_content = log_file.read_text(encoding="utf-8")

    assert "INFO" in log_content
    assert "WARNING" in log_content
    assert "ERROR" in log_content

    assert "multiply: 4, 5 = 20" in log_content
    assert "Test warning" in log_content
    assert "Test error" in log_content


def test_logging_observer_logger_configuration(tmp_path):
    """Test the logger's configuration."""
    log_file = tmp_path / "calculator.log"

    observer = LoggingObserver(log_file=log_file)

    assert observer.logger.level == logging.INFO
    assert observer.logger.propagate is False

    assert len(observer.logger.handlers) == 1
    assert isinstance(
        observer.logger.handlers[0],
        logging.FileHandler
    )
