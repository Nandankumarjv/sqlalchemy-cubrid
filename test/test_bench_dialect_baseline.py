from __future__ import annotations

import pytest
from scripts import bench_dialect_baseline as bdb


def test_summary_returns_expected_statistics() -> None:
    values = [10.0, 20.0, 30.0]

    result = bdb.summary(values)

    assert result["median"] == 20.0
    assert result["min"] == 10.0
    assert result["max"] == 30.0
    assert result["q1"] == 15.0
    assert result["q3"] == 25.0
    assert result["trials"] == values


def test_summary_handles_single_value() -> None:
    values = [42.0]

    result = bdb.summary(values)

    assert result["median"] == 42.0
    assert result["min"] == 42.0
    assert result["max"] == 42.0
    assert result["q1"] == 42.0
    assert result["q3"] == 42.0
    assert result["trials"] == values


def test_us_converts_median_nanoseconds_to_microseconds() -> None:
    assert bdb.us([1000, 2000, 3000]) == 2.0


@pytest.mark.parametrize(
    ("items", "trial", "expected"),
    [
        (["A", "B", "C"], 0, ["A", "B", "C"]),
        (["A", "B", "C"], 1, ["B", "C", "A"]),
        (["A", "B", "C"], 4, ["B", "C", "A"]),
    ],
)
def test_rotate_moves_items_by_trial(
    items: list[str],
    trial: int,
    expected: list[str],
) -> None:
    original = items.copy()

    result = bdb.rotate(items, trial)

    assert result == expected
    assert items == original
