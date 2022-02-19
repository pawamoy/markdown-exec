"""Formatter and utils for executing Python code."""

import traceback
from copy import deepcopy

from markdown.core import Markdown
from markupsafe import Markup


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


def exec_python(source: str, md: Markdown) -> str:
    """Execute code and return HTML.

    Parameters:
        source: The code to execute.
        md: The Markdown instance.

    Returns:
        HTML contents.
    """
    try:
        exec(source)  # noqa: S102
    except MarkdownOutput as output:
        return Markup(deepcopy(md).convert(str(output)))
    except HTMLOutput as output:
        return str(output)
    except Exception:
        return Markup(deepcopy(md).convert(f"```python\n{traceback.format_exc()}\n```"))
    return ""
