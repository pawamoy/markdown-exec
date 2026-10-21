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

import re
import sys
import traceback
from collections import defaultdict
from dataclasses import dataclass
from functools import partial
from io import StringIO
from types import ModuleType
from typing import TYPE_CHECKING, Any

from markdown_exec._internal.formatters._exec_python import exec_python, exec_python_interactive
from markdown_exec._internal.formatters.base import ExecutionError, base_format
from markdown_exec._internal.rendering import code_block

if TYPE_CHECKING:
    from collections.abc import Iterator

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


@dataclass(slots=True)
class InteractiveInput:
    """A single interactive input to the interpreter.

    May consist of one line or multiple lines (`>>>` followed by `...`).
    May contain multiple statements.
    """

    lineno: int
    display_lines: list[str]
    src_lines: list[str]

    @classmethod
    def split(cls, code: str, filename: str) -> Iterator[InteractiveInput]:
        lines = enumerate(code.split("\n"))
        current = None

        for lineno, line in lines:
            if line.startswith("... "):
                if current:
                    current.append(line)
                else:
                    raise SyntaxError("Expected '>>>'", (filename, lineno, 1, line, lineno, 4))
            else:
                if current:
                    yield current
                current = None

                if line.startswith(">>> "):
                    current = InteractiveInput.from_line(lineno, line)

        if current:
            yield current

    @classmethod
    def from_line(cls, lineno: int, line: str) -> InteractiveInput:
        return cls(lineno, [line], [line[4:]])

    def append(self, line: str) -> None:
        self.display_lines.append(line)
        self.src_lines.append(line[4:])

    def with_traceback(self, error: Exception) -> traceback.TracebackException:
        trace = traceback.TracebackException.from_exception(error)

        start = None
        for i, frame in enumerate(trace.stack):
            if frame.filename.startswith("<code block: ") and i > 0:
                if start is None:
                    start = i

                if sys.version_info >= (3, 13):
                    frame._lines = self.display_lines[frame.lineno - 1]  # ty:ignore[unresolved-attribute,unsupported-operator,unused-ignore-comment,unused-ignore-comment]
                else:
                    frame._line = self.display_lines[frame.lineno - 1]  # ty:ignore[unresolved-attribute,unsupported-operator,unused-ignore-comment,unused-ignore-comment]

                frame.lineno += self.lineno  # ty:ignore[unsupported-operator]

        if start is None:
            # If the traceback doesn't contain `<code block:` that means the error originated in this package
            raise error

        # Remove exec/eval frames from stack
        if start > 0:
            del trace.stack[:i]

        return trace


def _run_interactive(
    code: str,
    filename: str,
    global_vars: dict,
    buffer: StringIO,
) -> None:
    for inp in InteractiveInput.split(code, filename):
        buffer.write("\n".join(inp.display_lines) + "\n")
        try:
            if (res := exec_python_interactive("\n".join(inp.src_lines), filename, global_vars)) is not None:
                buffer.write(repr(res) + "\n")
        except Exception as error:
            if isinstance(error, SyntaxError):
                raise

            trace = inp.with_traceback(error)
            buffer.write("".join(trace.format()))


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

    if interactive:
        return code_block("pycon", buffer.getvalue())

    return buffer.getvalue()


def _format_python(**kwargs: Any) -> str:
    return base_format(language="python", run=_run_python, **kwargs)
