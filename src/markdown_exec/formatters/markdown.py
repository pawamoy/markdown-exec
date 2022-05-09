"""Formatter for reapply literate Markdown."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from markdown.core import Markdown

from markdown_exec.rendering import add_source, markdown


def format_markdown(  # noqa: WPS231
    code: str,
    md: Markdown,
    html: bool,
    source: str,
    tabs: tuple[str, str],
    **options: Any,
) -> str:
    """Reapply Markdown and return HTML.

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
    extra = options.get("extra", {})
    output = code
    stash = {}
    if html:
        placeholder = str(uuid4())
        stash[placeholder] = output
        output = placeholder
    if source:
        output = add_source(source=code, location=source, output=output, language="md", tabs=tabs, **extra)
    return markdown.convert(output, stash=stash)
