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

# Formatter for executing shell code.

from __future__ import annotations

import subprocess
from typing import Any

from markdown_exec._internal.formatters.base import ExecutionError, base_format
from markdown_exec._internal.rendering import code_block


def _run_sh(
    code: str,
    returncode: int | None = None,
    session: str | None = None,  # noqa: ARG001
    id: str | None = None,  # noqa: A002,ARG001
    **extra: str,
) -> str:
    process = subprocess.run(  # noqa: S603
        ["sh", "-c", code],  # noqa: S607
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
        encoding="utf8",
    )
    if process.returncode != returncode:
        raise ExecutionError(code_block("sh", process.stdout, **extra), process.returncode)
    return process.stdout


def _format_sh(**kwargs: Any) -> str:
    return base_format(language="sh", run=_run_sh, **kwargs)
