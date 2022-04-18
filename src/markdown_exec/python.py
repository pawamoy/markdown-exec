"""Formatter and utils for executing Python code."""

import traceback
from textwrap import indent
from typing import Any

from markdown.core import Markdown
from markupsafe import Markup

from markdown_exec.markdown_helpers import code_block, tabbed

md_copy = None


class MarkdownOutput(Exception):  # noqa: N818
    """Exception to return Markdown."""


class HTMLOutput(Exception):  # noqa: N818
    """Exception to return HTML."""


def output_markdown(text: str) -> None:
    """Output Markdown.

    Parameters:
        text: The Markdown to convert and inject back in the page.

    Raises:
        MarkdownOutput: Our way of returning without 'return' or 'yield' keywords.
    """
    raise MarkdownOutput(text)


def output_html(text: str) -> None:
    """Output HTML.

    Parameters:
        text: The HTML to inject back in the page.

    Raises:
        HTMLOutput: Our way of returning without 'return' or 'yield' keywords.
    """
    raise HTMLOutput(text)


def exec_python(  # noqa: WPS231
    source: str,
    md: Markdown,
    isolate: bool = False,
    show_source: str = "",
    **options: Any,
) -> str:
    """Execute code and return HTML.

    Parameters:
        source: The code to execute.
        md: The Markdown instance.
        isolate: Whether to run the code in isolation.
        show_source: Whether to show source as well, and where.
        **options: Additional options passed from the formatter.

    Returns:
        HTML contents.
    """
    global md_copy  # noqa: WPS420
    if md_copy is None:
        md_copy = Markdown()  # noqa: WPS442
        md_copy.registerExtensions(md.registeredExtensions, {})
    if isolate:
        exec_source = f"def _function():\n{indent(source, prefix=' ' * 4)}\n_function()\n"
    else:
        exec_source = source
    try:
        exec(exec_source)  # noqa: S102
    except MarkdownOutput as raised_output:
        output = str(raised_output)
    except HTMLOutput as raised_output:
        output = f'<div markdown="0">{str(raised_output)}</div>'
    except Exception:
        output = code_block("python", traceback.format_exc())
    if show_source:
        source_block = code_block("python", source)
    if show_source == "above":
        output = source_block + "\n\n" + output
    elif show_source == "below":
        output = output + "\n\n" + source_block
    elif show_source == "tabbed-left":
        output = tabbed(("Source", source_block), ("Result", output))
    elif show_source == "tabbed-right":
        output = tabbed(("Result", output), ("Source", source_block))
    return Markup(md_copy.convert(output))
