"""This module contains helpers to generate Markdown contents."""

from __future__ import annotations

from textwrap import indent


def code_block(language: str, source: str, **options: str) -> str:
    """Format source as a code block.

    Parameters:
        language: The code block language.
        source: The source code to format.
        **options: Additional options passed from the source, to add back to the generated code block.

    Returns:
        The formatted code block.
    """
    opts = " ".join(f'{opt_name}="{opt_value}"' for opt_name, opt_value in options.items())
    return f"```{language} {opts}\n{source}\n```"


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
