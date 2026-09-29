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

# Formatter for executing `pycon` code.

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from markdown_exec._internal.formatters.base import base_format
from markdown_exec._internal.formatters.python import _run_python

if TYPE_CHECKING:
    from markupsafe import Markup


def _transform_source(code: str) -> tuple[str, str]:
    python_lines = []
    pycon_lines = []
    for line in code.split("\n"):
        if line.startswith((">>> ", "... ")):
            pycon_lines.append(line)
            python_lines.append(line[4:])
    python_code = "\n".join(python_lines)
    return python_code, "\n".join(pycon_lines)


def _format_pycon(**kwargs: Any) -> Markup:
    return base_format(language="pycon", run=_run_python, transform_source=_transform_source, **kwargs)
