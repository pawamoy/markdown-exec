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

from pathlib import Path
from textwrap import dedent

import pytest
from markdown import Markdown


def test_zensical_theme_has_icons() -> None:
    """Check that Zensical's theme accessor exposes the icons directory."""
    config = pytest.importorskip("zensical.config")

    # Check the private API directly, even when Material supplies the formatter's icons.
    theme_dir = Path(config.get_builtin_theme_dir())

    assert (theme_dir / ".icons").is_dir()


def test_output_markdown(md: Markdown) -> None:
    """Assert we can highlight lines in the output.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```tree hl_lines="2"
            1
            2
            3
            ```
            """,
        ),
    )
    assert '<span class="hll">' in html
