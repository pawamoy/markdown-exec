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

"""Tests for headings."""

from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import pytest
from mkdocs.commands.build import build
from mkdocs.config import load_config

from markdown_exec import markdown_config

if TYPE_CHECKING:
    from pathlib import Path

    from markdown import Markdown


def test_headings_removal(md: Markdown) -> None:
    """Headings should leave no trace behind.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            === "File layout"

                ```tree
                ./
                    hello.md
                ```
            """,
        ),
    )
    assert 'class="markdown-exec"' not in html


@pytest.mark.parametrize("exec_first", [True, False])
def test_exec_block_with_mkdocstrings_headings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    exec_first: bool,
) -> None:
    """Build a page with an executed block and docstring headings containing inline code."""
    # Keep the plugin's saved configuration local to this build.
    monkeypatch.setattr(markdown_config, "exts", None)
    monkeypatch.setattr(markdown_config, "exts_config", None)

    config_file = tmp_path / "mkdocs.yml"
    config_file.write_text("site_name: Heading reproduction\n", encoding="utf-8")
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    # Four headings reproduce the invalid stash indices without a large package.
    (tmp_path / "repro97.py").write_text(
        dedent(
            '''\
            """Summary.

            # Heading `1`

            Text with `code`.

            # Heading `2`

            Text with `code again`.

            # Heading `3`

            Text with `code again and again`.

            # Heading `4`.

            Text with `code again and again again`.
            """
            ''',
        ),
        encoding="utf-8",
    )
    exec_block = '```python exec="1"\nprint("hello from the exec block")\n```'
    directive = "::: repro97"
    blocks = [exec_block, directive] if exec_first else [directive, exec_block]
    (docs_dir / "index.md").write_text("\n\n".join(blocks), encoding="utf-8")
    config = load_config(
        config_file=str(config_file),
        docs_dir=str(docs_dir),
        site_dir=str(tmp_path / "site"),
        plugins=[
            "markdown-exec",
            {"mkdocstrings": {"handlers": {"python": {"paths": [str(tmp_path)], "options": {"show_source": False}}}}},
        ],
        markdown_extensions=["toc", "pymdownx.superfences"],
    )

    build(config)

    # Both parts of the page render successfully, in either order.
    html = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
    assert "hello from the exec block" in html
    assert "Heading <code>1</code>" in html
    assert "Heading <code>4</code>." in html
