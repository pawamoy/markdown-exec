"""Formatter for executing Python code."""

from __future__ import annotations

import traceback
from functools import partial
from io import StringIO
from typing import Any

from markdown_exec.formatters.base import base_format
from markdown_exec.rendering import code_block


def _buffer_print(buffer: StringIO, *text: str, end: str = "\n", **kwargs: Any) -> None:
    buffer.write(" ".join(text) + end)


def _run_python(code: str, **extra: str) -> str:
    buffer = StringIO()
    exec_globals = {"print": partial(_buffer_print, buffer)}

    try:
        exec(code, exec_globals)  # noqa: S102
    except Exception as error:
        trace = traceback.TracebackException.from_exception(error)
        for frame in trace.stack:
            if frame.filename == "<string>":
                frame.filename = "<executed code block>"
                frame._line = code.split("\n")[frame.lineno - 1]  # type: ignore[attr-defined,operator]  # noqa: WPS437
        raise RuntimeError(code_block("python", "".join(trace.format()), **extra))
    return buffer.getvalue()


def _format_python(*args, **kwargs) -> str:
    return base_format("python", _run_python, *args, **kwargs)
