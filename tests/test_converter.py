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

"""Tests for the Markdown converter."""

from __future__ import annotations

import re
from textwrap import dedent
from typing import TYPE_CHECKING

import pytest
from markdown.extensions.toc import TocExtension

from markdown_exec import MarkdownConfig, markdown_config

if TYPE_CHECKING:
    from markdown import Markdown


def test_rendering_nested_blocks(md: Markdown) -> None:
    """Assert nested blocks are properly handled.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ````md exec="1"
            ```python exec="1"
            print("**Bold!**")
            ```
            ````
            """,
        ),
    )
    assert html == "<p><strong>Bold!</strong></p>"


@pytest.mark.parametrize("save_config", [True, False])
def test_rendering_with_zensical_previews(md: Markdown, monkeypatch: pytest.MonkeyPatch, save_config: bool) -> None:
    """Render nested blocks while keeping previews enabled on page links."""
    preview = pytest.importorskip("zensical.extensions.preview")
    links = pytest.importorskip("zensical.extensions.links")

    # Zensical configures previews, then adds link processing to the page renderer.
    extension_configs = {preview.PreviewExtension.name: {"targets": {"include": ["reference/api.md"]}}}
    extensions = [*md.registeredExtensions, preview.PreviewExtension.name]
    md.registerExtensions([preview.PreviewExtension.name], extension_configs)
    links.LinksExtension(path="index.md", use_directory_urls=True).extendMarkdown(md)

    # Cover both saved extension names and the fallback to registered instances.
    monkeypatch.setattr(markdown_config, "exts", extensions if save_config else None)
    monkeypatch.setattr(markdown_config, "exts_config", extension_configs if save_config else None)

    html = md.convert(
        dedent(
            """
            [API](reference/api.md)

            ````md exec="1"
            ```python exec="1"
            print("**Generated output**")
            ```
            ````
            """,
        ),
    )

    assert "<p><strong>Generated output</strong></p>" in html
    assert '<a data-preview="" href="reference/api/">API</a>' in html


def test_instantiating_config_singleton() -> None:
    """Assert that the Markdown config instances act as a singleton."""
    assert MarkdownConfig() is markdown_config
    markdown_config.save([], {})
    markdown_config.reset()


@pytest.mark.parametrize(
    ("id", "id_prefix", "expected"),
    [
        ("", None, 'id="exec-\\d+--heading"'),
        ("", "", 'id="heading"'),
        ("", "some-prefix-", 'id="some-prefix-heading"'),
        ("some-id", None, 'id="some-id-heading"'),
        ("some-id", "", 'id="heading"'),
        ("some-id", "some-prefix-", 'id="some-prefix-heading"'),
    ],
)
def test_prefixing_headings(md: Markdown, id: str, id_prefix: str | None, expected: str) -> None:  # noqa: A002
    """Assert that we prefix headings as specified.

    Parameters:
        md: A Markdown instance (fixture).
        id: The code block id.
        id_prefix: The code block id prefix.
        expected: The id we expect to find in the HTML.
    """
    TocExtension().extendMarkdown(md)
    prefix = f'idprefix="{id_prefix}"' if id_prefix is not None else ""
    html = md.convert(
        dedent(
            f"""
            ```python exec="1" id="{id}" {prefix}
            print("# HEADING")
            ```
            """,
        ),
    )
    assert re.search(expected, html)
