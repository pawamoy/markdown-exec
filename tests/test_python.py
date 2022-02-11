"""Tests for the `python` module."""

from markdown.core import Markdown


def test_output_markdown(md: Markdown) -> None:
    """Assert Markdown is converted to HTML.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        """
        ```python exec="yes"
        output_markdown("**Bold!**")
        ```
        """
    )
    assert "<strong>Bold!</strong>" in html


def test_output_html(md: Markdown) -> None:
    """Assert HTML is injected as is.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        """
        ```python exec="yes"
        output_html("**Bold!**")
        ```
        """
    )
    assert "**Bold!**" in html
