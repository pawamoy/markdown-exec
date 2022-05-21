"""Markdown extensions and helpers."""

from __future__ import annotations

from textwrap import indent
from xml.etree.ElementTree import Element

from markdown import Markdown
from markdown.treeprocessors import Treeprocessor
from markupsafe import Markup


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
        title = title.replace(r"\|", "|").strip()
        parts.append(f'=== "{title}"')
        parts.append(indent(text, prefix=" " * 4))
        parts.append("")
    return "\n".join(parts)


def add_source(  # noqa: WPS212
    *,
    source: str,
    location: str,
    output: str,
    language: str,
    tabs: tuple[str, str],
    **extra: str,
) -> str:
    """Add source code block to the output.

    Parameters:
        source: The source code block.
        location: Where to add the source (above, below, tabbed-left, tabbed-right, console).
        output: The current output.
        language: The code language.
        tabs: Tabs titles (if used).
        **extra: Extra options added back to source code block.

    Raises:
        ValueError: When the given location is not supported.

    Returns:
        The updated output.
    """
    if location == "console":
        return code_block(language, source + "\n" + output, **extra)

    source_block = code_block(language, source, **extra)
    if location == "above":
        return source_block + "\n\n" + output
    if location == "below":
        return output + "\n\n" + source_block
    if location == "material-block":
        # TODO: remove style once margins are fixed in Material for MkDocs
        style = 'style="margin-top: 0;"'
        return source_block + f'\n\n<div class="result" {style} markdown="1" >\n\n{output}\n\n</div>'

    source_tab_title, result_tab_title = tabs
    if location == "tabbed-left":
        return tabbed((source_tab_title, source_block), (result_tab_title, output))
    if location == "tabbed-right":
        return tabbed((result_tab_title, output), (source_tab_title, source_block))

    raise ValueError(f"unsupported location for sources: {location}")


# code taken from mkdocstrings, credits to @oprypin
class _IdPrependingTreeprocessor(Treeprocessor):
    """Prepend the configured prefix to IDs of all HTML elements."""

    name = "markdown_exec_ids"

    def __init__(self, md: Markdown, id_prefix: str):  # noqa: D107
        super().__init__(md)
        self.id_prefix = id_prefix

    def run(self, root: Element):  # noqa: D102,WPS231
        if not self.id_prefix:
            return
        for el in root.iter():
            id_attr = el.get("id")
            if id_attr:
                el.set("id", self.id_prefix + id_attr)

            href_attr = el.get("href")
            if href_attr and href_attr.startswith("#"):
                el.set("href", "#" + self.id_prefix + href_attr[1:])

            name_attr = el.get("name")
            if name_attr:
                el.set("name", self.id_prefix + name_attr)

            if el.tag == "label":
                for_attr = el.get("for")
                if for_attr:
                    el.set("for", self.id_prefix + for_attr)


def _mimic(md: Markdown) -> Markdown:
    new_md = Markdown()  # noqa: WPS442
    new_md.registerExtensions(md.registeredExtensions + ["tables", "md_in_html"], {})
    new_md.treeprocessors.register(
        _IdPrependingTreeprocessor(md, ""),
        _IdPrependingTreeprocessor.name,
        priority=4,  # right after 'toc' (needed because that extension adds ids to headers)
    )
    return new_md


class _MarkdownConverter:
    """Helper class to avoid breaking the original Markdown instance state."""

    def __init__(self) -> None:  # noqa: D107
        self._md_ref: Markdown = None  # type: ignore[assignment]
        self._md_stack: list[Markdown] = []
        self._counter: int = 0
        self._level: int = 0

    def setup(self, md: Markdown) -> None:
        if not self._md_ref:
            self._md_ref = md

    def convert(self, text: str, stash: dict[str, str] | None = None) -> Markup:
        """Convert Markdown text to safe HTML.

        Parameters:
            text: Markdown text.
            stash: An HTML stash.

        Returns:
            Safe HTML.
        """
        # store current md instance
        md = self._md
        self._level += 1

        # prepare for conversion
        md.treeprocessors[_IdPrependingTreeprocessor.name].id_prefix = f"exec-{self._counter}--"
        self._counter += 1

        try:  # noqa: WPS501
            converted = md.convert(text)
        finally:
            self._level -= 1
            md.treeprocessors[_IdPrependingTreeprocessor.name].id_prefix = ""

        # restore html from stash
        for placeholder, stashed in (stash or {}).items():
            converted = converted.replace(placeholder, stashed)

        return Markup(converted)

    @property
    def _md(self) -> Markdown:
        try:
            return self._md_stack[self._level]
        except IndexError:
            self._md_stack.append(_mimic(self._md_ref))
            return self._md


# provide a singleton
markdown = _MarkdownConverter()
