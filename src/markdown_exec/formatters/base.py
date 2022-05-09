"""Generic formatter for executing code."""

from __future__ import annotations

from typing import Any, Callable
from uuid import uuid4

from markdown.core import Markdown
from markupsafe import Markup

from markdown_exec.rendering import add_source, markdown


def base_format(  # noqa: WPS231
    language: str,
    run: Callable,
    code: str,
    md: Markdown,
    html: bool,
    source: str,
    tabs: tuple[str, str],
    **options: Any,
) -> Markup:
    """Execute code and return HTML.

    Parameters:
        language: The code language.
        run: Function that runs code and returns output.
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
    extra = options.get("extra", {})
    output = run(code, **extra)
    stash = {}
    if html:
        placeholder = str(uuid4())
        stash[placeholder] = output
        output = placeholder
    if source:
        output = add_source(source=code, location=source, output=output, language=language, tabs=tabs, **extra)
    return markdown.convert(output, stash=stash)