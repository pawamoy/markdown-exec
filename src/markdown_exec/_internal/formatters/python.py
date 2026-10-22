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
from textwrap import indent
from types import ModuleType
from typing import TYPE_CHECKING, Any

from markdown_exec._internal.formatters._exec_python import exec_python, exec_python_interactive
from markdown_exec._internal.formatters.base import ExecutionError, base_format
from markdown_exec._internal.logger import get_logger
from markdown_exec._internal.rendering import code_block

if TYPE_CHECKING:
    from collections.abc import Iterator

_logger = get_logger(__name__)
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
class _InteractiveInput:
    """A single interactive input to the interpreter.

    May consist of one line or multiple lines (`>>>` followed by `...`).
    May contain multiple statements.
    """

    lineno: int
    display_lines: list[str]
    src_lines: list[str]

    @classmethod
    def split(cls, code: str, filename: str) -> Iterator[_InteractiveInput]:
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
                    current = _InteractiveInput.from_line(lineno, line)

        if current:
            yield current

    @classmethod
    def from_line(cls, lineno: int, line: str) -> _InteractiveInput:
        return cls(lineno, [line], [line[4:]])

    def append(self, line: str) -> None:
        self.display_lines.append(line)
        self.src_lines.append(line[4:])

    def with_traceback(self, error: Exception) -> traceback.TracebackException:
        if isinstance(error, SyntaxError) and (error.filename or "").startswith("<code block: "):
            # Fix line and column for syntax errors originating in the code block
            error.text = self.display_lines[error.lineno - 1]  # ty:ignore[unsupported-operator]
            error.lineno += self.lineno  # ty:ignore[unsupported-operator]
            error.offset += 4  # ty:ignore[unsupported-operator]
            if error.end_lineno is not None:
                error.end_lineno += self.lineno
            if error.end_offset is not None:
                error.end_offset += 4

        trace = traceback.TracebackException.from_exception(error)

        start = None
        for i, frame in enumerate(trace.stack):
            if frame.filename.startswith("<code block: ") and i > 0:
                # Find first stack frame originating in the code block
                if start is None:
                    start = i

                if sys.version_info >= (3, 13):
                    frame._lines = self.display_lines[frame.lineno - 1]  # ty:ignore[unresolved-attribute,unsupported-operator,unused-ignore-comment,unused-ignore-comment]
                else:
                    frame._line = self.display_lines[frame.lineno - 1]  # ty:ignore[unresolved-attribute,unsupported-operator,unused-ignore-comment,unused-ignore-comment]

                # Fix line and column
                frame.colno += 4  # ty:ignore[unsupported-operator]
                frame.lineno += self.lineno  # ty:ignore[unsupported-operator]
                if frame.end_lineno is not None:
                    frame.end_lineno += self.lineno
                if frame.end_colno is not None:
                    frame.end_colno += 4

        if getattr(trace, "filename", "").startswith("<code block: ") and start is None:
            # Syntax errors sort of "skip" a stack frame
            # Need to check the error's filename to determine if it came from the code block
            start = len(trace.stack)

        if start is None:
            # Error originated from this package not the code block, so we need to reraise it
            raise error

        # Remove exec/eval frames from stack
        if start > 0:
            del trace.stack[:start]

        return trace


def _run_interactive(  # noqa: PLR0917
    code: str,
    filename: str,
    exec_globals: dict,
    buffer: StringIO,
    id: str | None,  # noqa: A002
    title: str | None,
) -> None:
    for inp in _InteractiveInput.split(code, filename):
        buffer.write("\n".join(inp.display_lines) + "\n")
        try:
            if (res := exec_python_interactive("\n".join(inp.src_lines), filename, exec_globals)) is not None:
                buffer.write(repr(res) + "\n")
        except Exception as error:  # noqa: BLE001
            trace = inp.with_traceback(error)
            err_msg = "".join(trace.format())
            # Write error traceback to output buffer
            buffer.write(err_msg)

            # Need to manually log the warning because we don't want to abort processing the block
            identifier = id or title
            identifier = identifier and f"'{identifier}'"
            log_err = indent(err_msg, " " * 2)
            log_message = f"Unexpected exception while executing pycon code block {identifier}:\n\n{log_err}"
            _logger.warning(log_message)


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
            _run_interactive(code, code_block_id, exec_globals, buffer, id, title)
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


def _format_python(
    *,
    # Pull out interactive flag to avoid passing to _run_python
    interactive: bool = False,  # noqa: ARG001
    **kwargs: Any,
) -> str:
    return base_format(language="python", run=_run_python, **kwargs)
