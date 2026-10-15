
"""Tests for the Calculator Memento Design Pattern."""

from app.calculation import Calculation
from app.history import CalculationHistory


def test_save_and_restore_history():
    history = CalculationHistory()

    history.add(Calculation("add", 10, 5))
    snapshot = history.save_state()

    history.add(Calculation("multiply", 4, 5))
    assert history.count() == 2

    history.restore_state(snapshot)

    assert history.count() == 1
    assert history.get_last().result == 15


def test_restore_empty_history():
    history = CalculationHistory()
    snapshot = history.save_state()

    history.add(Calculation("add", 10, 5))
    history.restore_state(snapshot)

    assert history.count() == 0
    assert history.get_all() == []


def test_memento_preserves_snapshot():
    history = CalculationHistory()
    history.add(Calculation("add", 10, 5))

    snapshot = history.save_state()
    history.clear()

    assert history.count() == 0
    assert len(snapshot.get_state()) == 1

def test_undo_restores_previous_history():
    history = CalculationHistory()
    history.add(Calculation("add", 10, 5))

    history.checkpoint()
    history.add(Calculation("multiply", 4, 5))

    assert history.count() == 2
    assert history.undo() is True
    assert history.count() == 1
    assert history.get_last().result == 15


def test_redo_restores_undone_history():
    history = CalculationHistory()
    history.add(Calculation("add", 10, 5))

    history.checkpoint()
    history.add(Calculation("multiply", 4, 5))

    history.undo()

    assert history.redo() is True
    assert history.count() == 2
    assert history.get_last().result == 20


def test_undo_redo_without_checkpoints():
    history = CalculationHistory()

    assert history.undo() is False
    assert history.redo() is False
