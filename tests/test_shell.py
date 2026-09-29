# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2022, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""Tests for the shell formatters."""

from __future__ import annotations

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
            ```sh exec="yes"
            echo "**Bold!**"
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
            ```sh exec="yes" html="yes"
            echo "**Bold!**"
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
            ```sh exec="yes"
            echo("wrong syntax")
            ```
            """,
        ),
    )
    assert "error" in html
    assert "Execution of sh code block exited with unexpected code 2" in caplog.text


def test_return_code(md: Markdown, caplog: pytest.LogCaptureFixture) -> None:
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
            """,
        ),
    )
    assert "Not in the mood" in html
    assert "exited with" not in caplog.text
