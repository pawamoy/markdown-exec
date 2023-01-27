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
    assert "error" in html
    assert "Execution of sh code block exited with unexpected code 2" in caplog.text


def test_return_code(md: Markdown, caplog) -> None:
    """Assert return code is used correctly.

    Parameters:
        md: A Markdown instance (fixture).
        caplog: Pytest fixture to capture logs.
    """
    html = md.convert(
        dedent(
            """
            ```sh exec="yes" returncode="1"
            echo Not in the mood
            exit 1
            ```
            """
        )
    )
    assert "Not in the mood" in html
    assert "exited with" not in caplog.text
