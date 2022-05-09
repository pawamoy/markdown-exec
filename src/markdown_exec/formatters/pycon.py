"""Formatter for executing `pycon` code."""

from __future__ import annotations

import textwrap
from typing import Any
from uuid import uuid4

from markdown.core import Markdown

from markdown_exec.formatters.python import run_python
from markdown_exec.rendering import add_source, markdown


def format_pycon(  # noqa: WPS231
    code: str,
    md: Markdown,
    html: bool,
    source: str,
    tabs: tuple[str, str],
    **options: Any,
) -> str:
    """Execute `pycon` code and return HTML.

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
    markdown.setup(md)

    python_lines = []
    for line in code.split("\n"):
        if line.startswith(">>> "):
            python_lines.append(line[4:])
    python_code = "\n".join(python_lines)

    extra = options.get("extra", {})
    output = run_python(python_code, **extra)
    stash = {}
    if html:
        placeholder = str(uuid4())
        stash[placeholder] = output
        output = placeholder
    if source:
        source_code = textwrap.indent(python_code, ">>> ")
        output = add_source(source=source_code, location=source, output=output, language="pycon", tabs=tabs, **extra)
    return markdown.convert(output, stash=stash)
