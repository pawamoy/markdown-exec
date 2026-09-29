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
    assert "big-heading" in md.toc  # ty:ignore[unresolved-attribute]


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
    assert "big-heading" not in md.toc  # ty:ignore[unresolved-attribute]


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
    assert "big-heading" not in md.toc  # ty:ignore[unresolved-attribute]
    assert "medium-heading" in md.toc  # ty:ignore[unresolved-attribute]
    assert "small-heading" not in md.toc  # ty:ignore[unresolved-attribute]
    assert "tiny-heading" in md.toc  # ty:ignore[unresolved-attribute]
