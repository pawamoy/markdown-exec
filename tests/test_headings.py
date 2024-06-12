"""Tests for headings."""

from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from markdown import Markdown


def test_headings_removal(md: Markdown) -> None:
    """Headings should leave no trace behind.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            === "File layout"

                ```tree
                ./
                    hello.md
                ```
            """,
        ),
    )
    assert 'class="markdown-exec"' not in html
