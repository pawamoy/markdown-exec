"""Tests for the Python formatters."""

from __future__ import annotations

import re
from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest
    from markdown import Markdown


def test_output_markdown(md: Markdown) -> None:
    """Assert Markdown is converted to HTML.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```python exec="yes"
            print("**Bold!**")
            ```
            """,
        ),
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
            ```python exec="yes" html="yes"
            print("**Bold!**")
            ```
            """,
        ),
    )
    assert html == "<p>**Bold!**\n</p>"


def test_error_raised(md: Markdown, caplog: pytest.LogCaptureFixture) -> None:
    """Assert errors properly log a warning and return a formatted traceback.

    Parameters:
        md: A Markdown instance (fixture).
        caplog: Pytest fixture to capture logs.
    """
    html = md.convert(
        dedent(
            """
            ```python exec="yes"
            raise ValueError("oh no!")
            ```
            """,
        ),
    )
    assert "Traceback" in html
    assert "ValueError" in html
    assert "oh no!" in html
    assert "Execution of python code block exited with errors" in caplog.text


def test_can_print_non_string_objects(md: Markdown) -> None:
    """Assert we can print non-string objects.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```python exec="yes"
            class NonString:
                def __str__(self):
                    return "string"

            nonstring = NonString()
            print(nonstring, nonstring)
            ```
            """,
        ),
    )
    assert "Traceback" not in html


def test_sessions(md: Markdown) -> None:
    """Assert sessions can be reused.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```python exec="1" session="a"
            a = 1
            ```

            ```pycon exec="1" session="b"
            >>> b = 2
            ```

            ```pycon exec="1" session="a"
            >>> print(f"a = {a}")
            >>> try:
            ...     print(b)
            ... except NameError:
            ...     print("ok")
            ... else:
            ...     print("ko")
            ```

            ```python exec="1" session="b"
            print(f"b = {b}")
            try:
                print(a)
            except NameError:
                print("ok")
            else:
                print("ko")
            ```
            """,
        ),
    )
    assert "a = 1" in html
    assert "b = 2" in html
    assert "ok" in html
    assert "ko" not in html


def test_reporting_errors_in_sessions(md: Markdown, caplog: pytest.LogCaptureFixture) -> None:
    """Assert errors and source lines are correctly reported across sessions.

    Parameters:
        md: A Markdown instance (fixture).
        caplog: Pytest fixture to capture logs.
    """
    html = md.convert(
        dedent(
            """
            ```python exec="1" session="a"
            def fraise():
                raise RuntimeError("strawberry")
            ```

            ```python exec="1" session="a"
            print("hello")
            fraise()
            ```
            """,
        ),
    )
    assert "Traceback" in html
    assert "strawberry" in html
    assert "fraise()" in caplog.text
    assert 'raise RuntimeError("strawberry")' in caplog.text


def test_removing_output_from_pycon_code(md: Markdown) -> None:
    """Assert output lines are removed from pycon snippets.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```pycon exec="1" source="console"
            >>> print("ok")
            ko
            ```
            """,
        ),
    )
    assert "ok" in html
    assert "ko" not in html


def test_functions_have_a_module_attribute(md: Markdown) -> None:
    """Assert functions have a `__module__` attribute.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```python exec="1"
            def func():
                pass

            print(f"`{func.__module__}`")
            ```
            """,
        ),
    )
    assert "_code_block_n" in html


def test_future_annotations_do_not_leak_into_user_code(md: Markdown) -> None:
    """Assert future annotations do not leak into user code.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```python exec="1"
            class Int:
                ...

            def f(x: Int) -> None:
                return x + 1.0

            print(f"`{f.__annotations__['x']}`")
            ```
            """,
        ),
    )
    assert "<code>Int</code>" not in html
    assert re.search(r"class '_code_block_n\d+_\.Int'", html)
