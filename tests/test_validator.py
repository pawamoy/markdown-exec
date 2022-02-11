"""Tests for the `validator` function."""

import pytest
from markdown.core import Markdown

from markdown_exec import validator


@pytest.mark.parametrize(
    ("exec_value", "expected"),
    [
        ("yes", True),
        ("YES", True),
        ("on", True),
        ("ON", True),
        ("whynot", True),
        ("true", True),
        ("TRUE", True),
        ("1", True),
        ("-1", True),
        ("0", False),
        ("no", False),
        ("NO", False),
        ("off", False),
        ("OFF", False),
        ("false", False),
        ("FALSE", False),
    ],
)
def test_validate(md: Markdown, exec_value: str, expected: bool) -> None:
    """Assert the validator returns True or False given inputs.

    Parameters:
        md: A Markdown instance.
        exec_value: The exec option value, passed from the code block.
        expected: Expected validation result.
    """
    assert validator("whatever", inputs={"exec": exec_value}, options={}, attrs={}, md=md) is expected
