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

"""Tests for the `validator` function."""

import pytest
from markdown.core import Markdown

from markdown_exec import validator


@pytest.mark.parametrize(
    ("exec_value", "expected"),
    [
        ("yes", True),
        ("YES", True),
        ("on", True),
        ("ON", True),
        ("whynot", True),
        ("true", True),
        ("TRUE", True),
        ("1", True),
        ("-1", True),
        ("0", False),
        ("no", False),
        ("NO", False),
        ("off", False),
        ("OFF", False),
        ("false", False),
        ("FALSE", False),
    ],
)
def test_validate(md: Markdown, exec_value: str, expected: bool) -> None:
    """Assert the validator returns True or False given inputs.

    Parameters:
        md: A Markdown instance.
        exec_value: The exec option value, passed from the code block.
        expected: Expected validation result.
    """
    assert validator("whatever", inputs={"exec": exec_value}, options={}, attrs={}, md=md) is expected
