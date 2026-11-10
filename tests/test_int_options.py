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

"""Tests for non-numeric integer options passed to the `validator` function."""

from markdown.core import Markdown

from markdown_exec import validator


def test_validator_invalid_returncode_falls_back_to_zero(md: Markdown) -> None:
    """Assert a non-numeric `returncode` option does not raise, and defaults to 0."""
    options: dict = {}
    assert (
        validator("python", inputs={"exec": "yes", "returncode": "abc"}, options=options, attrs={}, md=md)
        is True
    )
    assert options["returncode"] == 0


def test_validator_invalid_width_falls_back_to_zero(md: Markdown) -> None:
    """Assert a non-numeric `width` option does not raise, and defaults to 0."""
    options: dict = {}
    assert (
        validator("python", inputs={"exec": "yes", "width": "wide"}, options=options, attrs={}, md=md)
        is True
    )
    assert options["width"] == 0


def test_validator_valid_integers_still_parsed(md: Markdown) -> None:
    """Assert well-formed integer options keep their values."""
    options: dict = {}
    assert (
        validator("python", inputs={"exec": "yes", "returncode": "3", "width": "80"}, options=options, attrs={}, md=md)
        is True
    )
    assert options["returncode"] == 3
    assert options["width"] == 80
