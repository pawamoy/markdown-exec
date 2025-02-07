"""Tests for the TypeScript formatter."""

import platform
from textwrap import dedent

import pytest
from markdown import Markdown

from markdown_exec.formatters.base import ExecutionError
from markdown_exec.rendering import code_block


def _expect_error(md: Markdown, error_text: str, actual_html: str) -> None:
    """Utility function to check that the error text is formatted as expected."""
    expected_exception = ExecutionError(code_block("typescript", error_text))
    expected_html = md.convert(str(expected_exception))
    assert expected_html == actual_html


@pytest.mark.skipif(platform.python_version_tuple()[:2] >= ("3", "14"), reason="3.14 is still alpha and this doesn't work there yet")
def test_output_markdown(md: Markdown) -> None:
    """Test that output from code is rendered as Markdown."""
    html = md.convert(
        dedent(
            """
            ```typescript exec="yes"
            console.log("**Bold!**")
            ```
            """,
        ),
    )
    assert html == "<p><strong>Bold!</strong></p>"


@pytest.mark.skipif(platform.python_version_tuple()[:2] >= ("3", "14"), reason="3.14 is still alpha and this doesn't work there yet")
def test_session_persistence(md: Markdown) -> None:
    """Test that session data is persisted across code blocks."""
    html = md.convert(
        dedent(
            """
            ```typescript exec="1" session="a"
            let count = 0;
            ```

            ```typescript exec="1" session="a"
            count++;
            console.log(`Count: ${count}`);
            ```
            """,
        ),
    )
    assert "Count: 1" in html


@pytest.mark.skipif(platform.python_version_tuple()[:2] >= ("3", "14"), reason="3.14 is still alpha and this doesn't work there yet")
def test_runtime_error(md: Markdown, caplog: pytest.LogCaptureFixture) -> None:
    """Test that runtime errors are formatted correctly."""
    html = md.convert(
        dedent(
            """
            ```typescript exec="1" session="error-test"
            throw new Error("Intentional runtime error");
            ```
            """,
        ),
    )

    _expect_error(
        md,
        dedent(
            """
            Error: Intentional runtime error
                at <anonymous>:1:28
            """,
        ),
        html,
    )

    assert "Execution of typescript code block exited with errors" in caplog.text


@pytest.mark.skipif(platform.python_version_tuple()[:2] >= ("3", "14"), reason="3.14 is still alpha and this doesn't work there yet")
def test_type_error(md: Markdown, caplog: pytest.LogCaptureFixture) -> None:
    """Test that type errors are formatted correctly."""
    html = md.convert(
        dedent(
            """
            ```typescript exec="1"
            let count: number = "string";
            ```
            """,
        ),
    )

    _expect_error(
        md,
        dedent(
            """
              TS2322 [ERROR]: Type 'string' is not assignable to type 'number'.
              let count: number = "string";
                  ~~~~~
                  at <anonymous session>.ts:1:5

              error: Type checking failed.
            """,
        ),
        html,
    )

    assert "Execution of typescript code block exited with errors" in caplog.text


@pytest.mark.skipif(platform.python_version_tuple()[:2] >= ("3", "14"), reason="3.14 is still alpha and this doesn't work there yet")
def test_console_output(md: Markdown) -> None:
    """Test that console output is rendered correctly."""
    html = md.convert(
        dedent(
            """
            ```typescript exec="1"
            console.log("Hello");
            console.error("World");
            ```
            """,
        ),
    )
    assert "Hello" in html
    assert "World" in html


@pytest.mark.skipif(platform.python_version_tuple()[:2] >= ("3", "14"), reason="3.14 is still alpha and this doesn't work there yet")
def test_session_isolation(md: Markdown) -> None:
    """Test that sessions are isolated from each other."""
    html = md.convert(
        dedent(
            """
            ```typescript exec="1" session="session-a"
            let x = 1;
            console.log(`A: ${x}`);
            ```

            ```typescript exec="1" session="session-b"
            let x = 2;
            console.log(`B: ${x}`);
            ```

            ```typescript exec="1" session="session-a"
            console.log(`A2: ${x}`);
            ```
            """,
        ),
    )
    assert "A: 1" in html
    assert "B: 2" in html
    assert "A2: 1" in html


@pytest.mark.skipif(platform.python_version_tuple()[:2] >= ("3", "14"), reason="3.14 is still alpha and this doesn't work there yet")
def test_partial_execution(md: Markdown) -> None:
    """Test that partial execution works."""
    html = md.convert(
        dedent(
            """
            ```typescript exec="1" session="partial"
            let x = 1;
            console.log(`THE NUMBER IS ${x}`);
            throw new Error("Fail");
            x = 2;
            ```

            ```typescript exec="1" session="partial"
            console.log(`THE NUMBER IS ${x}`);
            ```
            """,
        ),
    )
    assert "THE NUMBER IS 1" in html
    assert "THE NUMBER IS 2" not in html


@pytest.mark.skipif(platform.python_version_tuple()[:2] >= ("3", "14"), reason="3.14 is still alpha and this doesn't work there yet")
def test_tscon_multiple_blocks(md: Markdown) -> None:
    """Test that multiple blocks of instructions are concatenated, as well as their output."""
    html = md.convert(
        dedent(
            """
            ```tscon exec="1"
            > const name: string = "Baron";
            > console.log(name);
            Baron
            > const age: string | number = "???";
            > console.log(age);
            ???
            ```
            """,
        ),
    )

    assert "Baron" in html
    assert "???" in html
