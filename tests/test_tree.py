"""Tests for the shell formatters."""

from textwrap import dedent

from markdown import Markdown


def test_output_markdown(md: Markdown) -> None:
    """Assert we can highlight lines in the output.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```tree hl_lines="2"
            1
            2
            3
            ```
            """
        )
    )
    assert '<span class="hll">' in html
