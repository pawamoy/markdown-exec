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

"""Tests for the octave formatter."""

from __future__ import annotations

from shutil import which
from textwrap import dedent
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from markdown import Markdown


pytestmark = pytest.mark.skipif(which("octave-cli") is None, reason="octave-cli is not installed")


def test_output_markdown(md: Markdown) -> None:
    """Assert Markdown is converted to HTML.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```octave exec="yes"
            disp("**Bold!**")
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
            ```octave exec="yes" html="yes"
            disp("**Bold!**")
            ```
            """,
        ),
    )
    assert html == "<p>**Bold!**\n</p>"


def test_output_with_invalid_history_file(md: Markdown, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Assert history-file errors do not appear in rendered output."""
    # A directory cannot be used as a history file.
    monkeypatch.setenv("OCTAVE_HISTFILE", str(tmp_path))

    html = md.convert(
        dedent(
            """
            ```octave exec="yes" html="yes"
            disp("**Bold!**")
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
            ```octave exec="yes"
            print("wrong syntax")
            ```
            """,
        ),
    )
    assert "error" in html
    assert "Execution of octave code block exited with unexpected code 1" in caplog.text


def test_return_code(md: Markdown, caplog: pytest.LogCaptureFixture) -> None:
    """Assert return code is used correctly.

    Parameters:
        md: A Markdown instance (fixture).
        caplog: Pytest fixture to capture logs.
    """
    html = md.convert(
        dedent(
            """
            ```octave exec="yes" returncode="2"
            disp('Not in the mood')
            exit(2)
            ```
            """,
        ),
    )
    assert "Not in the mood" in html
    assert "exited with" not in caplog.text
