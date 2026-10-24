
from __future__ import annotations

import ast
import statistics
from pathlib import Path
from typing import Any

import pytest


def load_helpers() -> dict[str, Any]:
    script = Path(__file__).resolve().parents[1] / "scripts" / "bench_dialect_baseline.py"
    tree = ast.parse(script.read_text(encoding="utf-8"))

    helper_names = {"summary", "us", "rotate"}
    helper_nodes = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in helper_names
    ]

    namespace: dict[str, Any] = {
        "statistics": statistics,
        "Any": Any,
    }
    module = ast.Module(body=helper_nodes, type_ignores=[])
    exec(compile(module, str(script), "exec"), namespace)
    return namespace


@pytest.fixture
def helpers() -> dict[str, Any]:
    return load_helpers()


def test_summary_returns_expected_statistics(helpers: dict[str, Any]) -> None:
    values = [10.0, 20.0, 30.0]

    result = helpers["summary"](values)

    assert result["median"] == 20.0
    assert result["min"] == 10.0
    assert result["max"] == 30.0
    assert result["q1"] == 15.0
    assert result["q3"] == 25.0
    assert result["trials"] == values


def test_summary_handles_single_value(helpers: dict[str, Any]) -> None:
    values = [42.0]

    result = helpers["summary"](values)

    assert result["median"] == 42.0
    assert result["min"] == 42.0
    assert result["max"] == 42.0
    assert result["q1"] == 42.0
    assert result["q3"] == 42.0
    assert result["trials"] == values


def test_us_converts_median_nanoseconds_to_microseconds(
    helpers: dict[str, Any],
) -> None:
    assert helpers["us"]([1000, 2000, 3000]) == 2.0


@pytest.mark.parametrize(
    ("items", "trial", "expected"),
    [
        (["A", "B", "C"], 0, ["A", "B", "C"]),
        (["A", "B", "C"], 1, ["B", "C", "A"]),
        (["A", "B", "C"], 4, ["B", "C", "A"]),
    ],
)
def test_rotate_moves_items_by_trial(
    helpers: dict[str, Any],
    items: list[str],
    trial: int,
    expected: list[str],
) -> None:
    assert helpers["rotate"](items, trial) == expected
