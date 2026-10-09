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

import pytest
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


@pytest.mark.parametrize(
    ("heading", "expected_name", "expected_html"),
    [
        ("Heading &mdash;", "Heading &mdash;", "Heading &mdash;"),
        (
            "Heading **&mdash;** tail &copy;",
            "Heading &mdash; tail &copy;",
            "Heading <strong>&mdash;</strong> tail &copy;",
        ),
        ("Heading <span>inline</span>", "Heading inline", "Heading <span>inline</span>"),
        ("Heading `*code*`", "Heading *code*", "Heading <code>*code*</code>"),
        ("&mdash;", "&mdash;", "&mdash;"),
    ],
)
def test_generated_headings_keep_stashed_content(
    md: Markdown,
    heading: str,
    expected_name: str,
    expected_html: str,
) -> None:
    """Keep heading content when the inner and outer HTML stashes use the same IDs."""
    TocExtension(permalink=True).extendMarkdown(md)

    # Entities and inline HTML belong to the generated block's Markdown instance.
    source = f'```md exec="1" idprefix=""\n# {heading}\n```'

    html = md.convert(source)

    # The page keeps the rendered heading, and its ToC uses the same content.
    assert '<h1 id="' in html
    assert expected_html in html
    assert md.toc_tokens[0]["name"] == expected_name  # ty:ignore[unresolved-attribute]
    assert md.toc_tokens[0]["html"] == expected_html  # ty:ignore[unresolved-attribute]
    assert expected_name in md.toc  # ty:ignore[unresolved-attribute]
    assert "wzxhzdk" not in html
