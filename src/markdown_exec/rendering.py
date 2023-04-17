"""Markdown extensions and helpers."""

from __future__ import annotations

from functools import lru_cache
from itertools import chain
from textwrap import indent
from typing import TYPE_CHECKING

from markdown import Markdown
from markupsafe import Markup

from markdown_exec.processors import (
    HeadingReportingTreeprocessor,
    IdPrependingTreeprocessor,
    InsertHeadings,
    RemoveHeadings,
)

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element

    from markdown import Extension


def code_block(language: str, code: str, **options: str) -> str:
    """Format code as a code block.

    Parameters:
        language: The code block language.
        code: The source code to format.
        **options: Additional options passed from the source, to add back to the generated code block.

    Returns:
        The formatted code block.
    """
    opts = " ".join(f'{opt_name}="{opt_value}"' for opt_name, opt_value in options.items())
    return f"````````{language} {opts}\n{code}\n````````"


def tabbed(*tabs: tuple[str, str]) -> str:
    """Format tabs using `pymdownx.tabbed` extension.

    Parameters:
        *tabs: Tuples of strings: title and text.

    Returns:
        The formatted tabs.
    """
    parts = []
    for title, text in tabs:
        title = title.replace(r"\|", "|").strip()  # noqa: PLW2901
        parts.append(f'=== "{title}"')
        parts.append(indent(text, prefix=" " * 4))
        parts.append("")
    return "\n".join(parts)


def _hide_lines(source: str) -> str:
    return "\n".join(line for line in source.split("\n") if "markdown-exec: hide" not in line).strip()


def add_source(
    *,
    source: str,
    location: str,
    output: str,
    language: str,
    tabs: tuple[str, str],
    result: str = "",
    **extra: str,
) -> str:
    """Add source code block to the output.

    Parameters:
        source: The source code block.
        location: Where to add the source (above, below, tabbed-left, tabbed-right, console).
        output: The current output.
        language: The code language.
        tabs: Tabs titles (if used).
        result: Syntax to use when concatenating source and result with "console" location.
        **extra: Extra options added back to source code block.

    Raises:
        ValueError: When the given location is not supported.

    Returns:
        The updated output.
    """
    source = _hide_lines(source)
    if location == "console":
        return code_block(result or language, source + "\n" + output, **extra)

    source_block = code_block(language, source, **extra)
    if location == "above":
        return source_block + "\n\n" + output
    if location == "below":
        return output + "\n\n" + source_block
    if location == "material-block":
        return source_block + f'\n\n<div class="result" markdown="1" >\n\n{output}\n\n</div>'

    source_tab_title, result_tab_title = tabs
    if location == "tabbed-left":
        return tabbed((source_tab_title, source_block), (result_tab_title, output))
    if location == "tabbed-right":
        return tabbed((result_tab_title, output), (source_tab_title, source_block))

    raise ValueError(f"unsupported location for sources: {location}")


@lru_cache(maxsize=None)
def _register_headings_processors(md: Markdown) -> None:
    md.treeprocessors.register(
        InsertHeadings(md),
        InsertHeadings.name,
        priority=75,  # right before markdown.blockprocessors.HashHeaderProcessor
    )
    md.treeprocessors.register(
        RemoveHeadings(md),
        RemoveHeadings.name,
        priority=4,  # right after toc
    )


def _mimic(md: Markdown, headings: list[Element], *, update_toc: bool = True) -> Markdown:
    new_md = Markdown()
    extensions: list[Extension | str] = list(chain(md.registeredExtensions, ["tables", "md_in_html"]))
    new_md.registerExtensions(extensions, {})
    new_md.treeprocessors.register(
        IdPrependingTreeprocessor(md, ""),
        IdPrependingTreeprocessor.name,
        priority=4,  # right after 'toc' (needed because that extension adds ids to headings)
    )
    new_md._original_md = md  # type: ignore[attr-defined]

    if update_toc:
        _register_headings_processors(md)
        new_md.treeprocessors.register(
            HeadingReportingTreeprocessor(new_md, headings),
            HeadingReportingTreeprocessor.name,
            priority=1,  # Close to the end.
        )

    return new_md


class MarkdownConverter:
    """Helper class to avoid breaking the original Markdown instance state."""

    counter: int = 0

    def __init__(self, md: Markdown, *, update_toc: bool = True) -> None:  # noqa: D107
        self._md_ref: Markdown = md
        self._headings: list[Element] = []
        self._update_toc = update_toc

    @property
    def _original_md(self) -> Markdown:
        return getattr(self._md_ref, "_original_md", self._md_ref)

    def convert(self, text: str, stash: dict[str, str] | None = None) -> Markup:
        """Convert Markdown text to safe HTML.

        Parameters:
            text: Markdown text.
            stash: An HTML stash.

        Returns:
            Safe HTML.
        """
        md = _mimic(self._original_md, self._headings, update_toc=self._update_toc)

        # prepare for conversion
        md.treeprocessors[IdPrependingTreeprocessor.name].id_prefix = f"exec-{MarkdownConverter.counter}--"
        MarkdownConverter.counter += 1

        try:
            converted = md.convert(text)
        finally:
            md.treeprocessors[IdPrependingTreeprocessor.name].id_prefix = ""

        # restore html from stash
        for placeholder, stashed in (stash or {}).items():
            converted = converted.replace(placeholder, stashed)

        markup = Markup(converted)

        # pass headings to upstream conversion layer
        if self._update_toc:
            self._original_md.treeprocessors[InsertHeadings.name].headings[markup] = self.headings

        return markup

    @property
    def headings(self) -> list[Element]:  # noqa: D102
        headings = self._headings
        self._headings = []
        return headings
