"""Tests for the shell formatters."""

from textwrap import dedent

from markdown import Markdown


def test_output_markdown(md: Markdown) -> None:
    """Assert Markdown is converted to HTML.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```sh exec="yes"
            echo "**Bold!**"
            ```
            """
        )
    )
    assert html == "<p><strong>Bold!</strong></p>"


def test_output_html(md: Markdown) -> None:
    """Assert HTML is injected as is.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```sh exec="yes" html="yes"
            echo "**Bold!**"
            ```
            """
        )
    )
    assert html == "<p>**Bold!**\n</p>"


def test_error_raised(md: Markdown, caplog) -> None:
    """Assert errors properly log a warning and return a formatted traceback.

    Parameters:
        md: A Markdown instance (fixture).
        caplog: Pytest fixture to capture logs.
    """
    html = md.convert(
        dedent(
            """
            ```sh exec="yes"
            echo("wrong syntax")
            ```
            """
        )
    )
    assert "syntax error near unexpected token" in html
    assert "Execution of sh code block exited with non-zero status" in caplog.text
