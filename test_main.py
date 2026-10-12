from datetime import date, timedelta

import pytest

from main import add_habit, complete_habit, calculate_streak


def test_add_habit():
    habits = {}

    add_habit(habits, "Exercise")

    assert "Exercise" in habits
    assert habits["Exercise"]["completed_dates"] == []


def test_add_empty_habit():
    with pytest.raises(ValueError):
        add_habit({}, "   ")


def test_add_duplicate_habit():
    habits = {}
    add_habit(habits, "Reading")

    with pytest.raises(ValueError):
        add_habit(habits, "Reading")


def test_complete_habit():
    habits = {}
    add_habit(habits, "Exercise")

    today = date(2026, 10, 12)
    complete_habit(habits, "Exercise", today)

    assert today.isoformat() in habits["Exercise"]["completed_dates"]


def test_completing_twice_does_not_duplicate_date():
    habits = {}
    add_habit(habits, "Reading")

    today = date(2026, 10, 12)

    complete_habit(habits, "Reading", today)
    complete_habit(habits, "Reading", today)

    assert habits["Reading"]["completed_dates"].count(
        today.isoformat()
    ) == 1


def test_calculate_three_day_streak():
    habits = {}
    add_habit(habits, "Exercise")

    today = date(2026, 10, 12)

    for days_ago in range(3):
        completed_day = today - timedelta(days=days_ago)
        complete_habit(habits, "Exercise", completed_day)

    assert calculate_streak(habits, "Exercise", today) == 3


def test_streak_breaks_when_a_day_is_missing():
    habits = {}
    add_habit(habits, "Exercise")

    today = date(2026, 10, 12)

    complete_habit(habits, "Exercise", today)
    complete_habit(
        habits,
        "Exercise",
        today - timedelta(days=2)
    )

    assert calculate_streak(habits, "Exercise", today) == 1


def test_unknown_habit():
    with pytest.raises(ValueError):
        complete_habit({}, "Unknown")