"""Generic formatter for executing code."""

from __future__ import annotations

from typing import Any, Callable
from uuid import uuid4

from markdown.core import Markdown
from markupsafe import Markup

from markdown_exec.logger import get_logger
from markdown_exec.rendering import MarkdownConverter, add_source, code_block

logger = get_logger(__name__)


def base_format(  # noqa: WPS231
    language: str,
    run: Callable,
    code: str,
    md: Markdown,
    html: bool,
    source: str,
    result: str,
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
        result: If provided, use as language to format result in a code block.
        tabs: Titles of tabs (if used).
        **options: Additional options passed from the formatter.

    Returns:
        HTML contents.
    """
    markdown = MarkdownConverter(md)
    extra = options.get("extra", {})
    try:
        output = run(code, **extra)
    except RuntimeError as error:
        logger.warning(f"Execution of {language} code block exited with non-zero status")
        return markdown.convert(str(error))
    if html and source:
        placeholder = str(uuid4())
        wrapped_output = add_source(
            source=code, location=source, output=placeholder, language=language, tabs=tabs, **extra
        )
        markup = markdown.convert(wrapped_output, stash={placeholder: output})
    elif html:
        markup = Markup(output)
    elif result:
        wrapped_output = code_block(result, output)
        markup = markdown.convert(wrapped_output)
    else:
        markup = markdown.convert(output)
    return markup
