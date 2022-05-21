"""Formatter for executing `pycon` code."""

from __future__ import annotations

import textwrap
from typing import Any
from uuid import uuid4

from markdown.core import Markdown

from markdown_exec.formatters.python import _run_python  # noqa: WPS450
from markdown_exec.logger import get_logger
from markdown_exec.rendering import add_source, code_block, markdown

logger = get_logger(__name__)


def _format_pycon(  # noqa: WPS231
    code: str,
    md: Markdown,
    html: bool,
    source: str,
    result: str,
    tabs: tuple[str, str],
    **options: Any,
) -> str:
    markdown.setup(md)

    python_lines = []
    for line in code.split("\n"):
        if line.startswith(">>> "):
            python_lines.append(line[4:])
    python_code = "\n".join(python_lines)

    extra = options.get("extra", {})
    try:
        output = _run_python(python_code, **extra)
    except RuntimeError as error:
        logger.warning("Execution of pycon code block exited with non-zero status")
        return markdown.convert(str(error))
    stash = {}
    if html:
        placeholder = str(uuid4())
        stash[placeholder] = output
        output = placeholder
    elif result:
        output = code_block(result, output)
    if source:
        source_code = textwrap.indent(python_code, ">>> ")
        output = add_source(source=source_code, location=source, output=output, language="pycon", tabs=tabs, **extra)
    return markdown.convert(output, stash=stash)
