"""Formatter for executing Python code."""

from __future__ import annotations

import traceback
from functools import partial
from io import StringIO
from typing import Any

from markdown.core import Markdown

from markdown_exec.rendering import add_source, code_block, markdown


def buffer_print(buffer: StringIO, *text: str, end: str = "\n", **kwargs: Any) -> None:
    """Print Markdown.

    Parameters:
        buffer: A string buffer to write into.
        *text: The text to write into the buffer. Multiple strings accepted.
        end: The string to write at the end.
        **kwargs: Other keyword arguments passed to `print` are ignored.
    """
    buffer.write(" ".join(text) + end)


def run_python(code: str, html: bool, **extra: str) -> str:
    """Run Python code using `exec` and return its output.

    Parameters:
        code: The code to execute.
        html: Whether the output is HTML.
        **extra: Extra options passed to the traceback code block in case of errors.

    Returns:
        The output.
    """
    buffer = StringIO()
    exec_globals = {"print": partial(buffer_print, buffer)}

    try:
        exec(code, {}, exec_globals)  # noqa: S102
    except Exception as error:
        trace = traceback.TracebackException.from_exception(error)
        for frame in trace.stack:
            if frame.filename == "<string>":
                frame.filename = "<executed code block>"
                frame._line = code.split("\n")[frame.lineno - 1]  # type: ignore[attr-defined,operator]  # noqa: WPS437
        output = code_block("python", "".join(trace.format()), **extra)
    else:
        output = buffer.getvalue()
        if html:
            output = f'<div markdown="0">{str(output)}</div>'
    return output


def format_python(  # noqa: WPS231
    code: str,
    md: Markdown,
    html: bool,
    source: str,
    tabs: tuple[str, str],
    **options: Any,
) -> str:
    """Execute `python` code and return HTML.

    Parameters:
        code: The code to execute.
        md: The Markdown instance.
        html: Whether to inject output as HTML directly, without rendering.
        source: Whether to show source as well, and where.
        tabs: Titles of tabs (if used).
        **options: Additional options passed from the formatter.

    Returns:
        HTML contents.
    """
    markdown.mimic(md)
    extra = options.get("extra", {})
    output = run_python(code, html, **extra)
    if source:
        output = add_source(source=code, location=source, output=output, language="python", tabs=tabs, **extra)
    return markdown.convert(output)
