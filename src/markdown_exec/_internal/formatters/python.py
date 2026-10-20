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

# Formatter for executing Python code.

from __future__ import annotations

import ast
import re
import sys
import traceback
from collections import defaultdict
from functools import partial
from io import StringIO
from types import ModuleType
from typing import Any

from markdown_exec._internal.formatters._exec_python import exec_python
from markdown_exec._internal.formatters.base import ExecutionError, base_format
from markdown_exec._internal.rendering import code_block

_sessions_globals: dict[str, dict] = defaultdict(dict)
_sessions_counter: dict[str | None, int] = defaultdict(int)
_code_blocks: dict[str, list[str]] = {}


def _buffer_print(buffer: StringIO, *texts: str, end: str = "\n", **kwargs: Any) -> None:  # noqa: ARG001
    buffer.write(" ".join(str(text) for text in texts) + end)


def _code_block_id(
    id: str | None = None,  # noqa: A002
    session: str | None = None,
    title: str | None = None,
) -> str:
    _sessions_counter[session] += 1
    if id:
        code_block_id = f"id {id}"
    elif session:
        code_block_id = f"session {session}; n{_sessions_counter[session]}"
        if title:
            code_block_id = f"{code_block_id}; title {title}"
    else:
        code_block_id = f"n{_sessions_counter[session]}"
        if title:
            code_block_id = f"{code_block_id}; title {title}"
    return f"<code block: {code_block_id}>"


def _exec_statement(
    lines: list[str],
    filename: str,
    global_vars: dict,
) -> str | None:
    cmd = ast.parse("\n".join(lines), filename, "exec")

    for stmt in cmd.body:
        if isinstance(stmt, ast.Expr):
            res = eval(  # noqa: S307
                compile(ast.Expression(stmt.value), filename, "eval"),
                global_vars,
            )
            if res is not None:
                return repr(res)
        else:
            exec(  # noqa: S102
                compile(ast.Module([stmt], []), filename, "exec"),
                global_vars,
            )
    return None


def _run_interactive(
    code: str,
    filename: str,
    global_vars: dict,
    buffer: StringIO,
) -> None:
    exprs = []
    for lineno, line in enumerate(code.split("\n")):
        if line.startswith(">>> "):
            exprs.append((lineno, [line], [line[4:]]))
        if line.startswith("... "):
            exprs[-1][1].append(line)
            exprs[-1][2].append(line[4:])

    for lineno, display_lines, src_lines in exprs:
        buffer.write("\n".join(display_lines) + "\n")
        try:
            if (res := _exec_statement(src_lines, filename, global_vars)) is not None:
                buffer.write(res + "\n")
        except Exception as error:
            if isinstance(error, SyntaxError):
                raise

            trace = traceback.TracebackException.from_exception(error)
            # Remove exec/eval frames from stack
            del trace.stack[:2]
            for frame in trace.stack:
                if frame.filename.startswith("<code block: "):
                    if sys.version_info >= (3, 13):
                        frame._lines = display_lines[frame.lineno - 1]
                    else:
                        frame._line = display_lines[frame.lineno - 1]

                    frame.lineno += lineno

            buffer.write("".join(trace.format()))

    out = code_block("pycon", buffer.getvalue())
    buffer.seek(0)
    buffer.write(out)


def _run_python(
    code: str,
    returncode: int | None = None,  # noqa: ARG001
    session: str | None = None,
    id: str | None = None,  # noqa: A002
    interactive: bool = False,  # noqa: FBT001, FBT002
    **extra: str,
) -> str:
    title = extra.get("title")
    code_block_id = _code_block_id(id, session, title)
    _code_blocks[code_block_id] = code.split("\n")
    exec_globals = _sessions_globals[session] if session else {}

    # Other libraries expect functions to have a valid `__module__` attribute.
    # To achieve this, we need to add a `__name__` attribute to the globals.
    # We compute the name from the code block ID, replacing invalid characters with `_`.
    # We also create a module object with the same name and add it to `sys.modules`,
    # because that's what yet other libraries expect (`dataclasses` for example).
    module_name = re.sub(r"[^a-zA-Z\d]+", "_", code_block_id)
    exec_globals["__name__"] = module_name
    sys.modules[module_name] = ModuleType(module_name)

    buffer = StringIO()
    exec_globals["print"] = partial(_buffer_print, buffer)

    try:
        if interactive:
            _run_interactive(code, code_block_id, exec_globals, buffer)
        else:
            exec_python(code, code_block_id, exec_globals)
    except Exception as error:
        trace = traceback.TracebackException.from_exception(error)
        for frame in trace.stack:
            if frame.filename.startswith("<code block: "):
                if sys.version_info >= (3, 13):
                    frame._lines = _code_blocks[frame.filename][frame.lineno - 1]  # ty:ignore[unresolved-attribute,unsupported-operator,unused-ignore-comment,unused-ignore-comment]
                else:
                    frame._line = _code_blocks[frame.filename][frame.lineno - 1]  # ty:ignore[unresolved-attribute,unsupported-operator,unused-ignore-comment,unused-ignore-comment]
        raise ExecutionError(code_block("python", "".join(trace.format()), **extra)) from error
    return buffer.getvalue()


def _format_python(**kwargs: Any) -> str:
    return base_format(language="python", run=_run_python, **kwargs)
