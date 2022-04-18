"""This module contains helpers to generate Markdown contents."""

from __future__ import annotations

from textwrap import indent


def code_block(language: str, source: str) -> str:
    """Format source as a code block.

    Parameters:
        language: The code block language.
        source: The source code to format.

    Returns:
        The formatted code block.
    """
    return f"```{language}\n{source}\n```"


def tabbed(*tabs: tuple[str, str]) -> str:
    """Format tabs using `pymdownx.tabbed` extension.

    Parameters:
        *tabs: Tuples of strings: title and text.

    Returns:
        The formatted tabs.
    """
    parts = []
    for title, text in tabs:
        parts.append(f'=== "{title}"')
        parts.append(indent(text, prefix=" " * 4))
        parts.append("")
    return "\n".join(parts)
