"""Test addition module."""

from sample_project.add import add


def test_add() -> None:
    result = add(5, 5)

    assert result == 10
