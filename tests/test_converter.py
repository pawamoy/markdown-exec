"""Tests for the Markdown converter."""

from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markdown import Markdown


def test_rendering_nested_blocks(md: Markdown) -> None:
    """Assert nested blocks are properly handled.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ````md exec="1"
            ```python exec="1"
            print("**Bold!**")
            ```
            ````
            """,
        ),
    )
    assert html == "<p><strong>Bold!</strong></p>"
