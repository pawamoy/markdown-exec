"""Tests for the logic updating the table of contents."""

from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

from markdown.extensions.toc import TocExtension

if TYPE_CHECKING:
    from markdown import Markdown


def test_updating_toc(md: Markdown) -> None:
    """Assert ToC is updated with generated headings.

    Parameters:
        md: A Markdown instance (fixture).
    """
    TocExtension().extendMarkdown(md)
    html = md.convert(
        dedent(
            """
            ```python exec="yes"
            print("# big heading")
            ```
            """,
        ),
    )
    assert "<h1" in html
    assert "big-heading" in md.toc  # type: ignore[attr-defined]


def test_not_updating_toc(md: Markdown) -> None:
    """Assert ToC is not updated with generated headings.

    Parameters:
        md: A Markdown instance (fixture).
    """
    TocExtension().extendMarkdown(md)
    html = md.convert(
        dedent(
            """
            ```python exec="yes" updatetoc="no"
            print("# big heading")
            ```
            """,
        ),
    )
    assert "<h1" in html
    assert "big-heading" not in md.toc  # type: ignore[attr-defined]


def test_both_updating_and_not_updating_toc(md: Markdown) -> None:
    """Assert ToC is not updated with generated headings.

    Parameters:
        md: A Markdown instance (fixture).
    """
    TocExtension().extendMarkdown(md)
    html = md.convert(
        dedent(
            """
            ```python exec="yes" updatetoc="no"
            print("# big heading")
            ```

            ```python exec="yes" updatetoc="yes"
            print("## medium heading")
            ```

            ```python exec="yes" updatetoc="no"
            print("### small heading")
            ```

            ```python exec="yes" updatetoc="yes"
            print("#### tiny heading")
            ```
            """,
        ),
    )
    assert "<h1" in html
    assert "<h2" in html
    assert "<h3" in html
    assert "<h4" in html
    assert "big-heading" not in md.toc  # type: ignore[attr-defined]
    assert "medium-heading" in md.toc  # type: ignore[attr-defined]
    assert "small-heading" not in md.toc  # type: ignore[attr-defined]
    assert "tiny-heading" in md.toc  # type: ignore[attr-defined]
