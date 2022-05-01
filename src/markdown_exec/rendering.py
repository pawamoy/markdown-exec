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
    return f"```{language} {opts}\n{code}\n```"


def tabbed(*tabs: tuple[str, str]) -> str:
    """Format tabs using `pymdownx.tabbed` extension.

    Parameters:
        *tabs: Tuples of strings: title and text.

    Returns:
        The formatted tabs.
    """
    parts = []
    for title, text in tabs:
        title = title.replace("\\|", "|").strip()
        parts.append(f'=== "{title}"')
        parts.append(indent(text, prefix=" " * 4))
        parts.append("")
    return "\n".join(parts)


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


class _MarkdownConverter:
    """Helper class to avoid breaking the original Markdown instance state."""

    def __init__(self) -> None:  # noqa: D107
        self.md: Markdown = None
        self.counter: int = 0

    def mimic(self, md: Markdown) -> None:
        """Mimic the passed Markdown instance by registering the same extensions.

        Parameters:
            md: A Markdown instance.
        """
        if self.md is None:
            self.md = Markdown()  # noqa: WPS442
            self.md.registerExtensions(md.registeredExtensions + ["pymdownx.extra"], {})
            self.md.treeprocessors.register(
                _IdPrependingTreeprocessor(md, ""),
                _IdPrependingTreeprocessor.name,
                priority=4,  # right after 'toc' (needed because that extension adds ids to headers)
            )

    def convert(self, text: str) -> Markup:
        """Convert Markdown text to safe HTML.

        Parameters:
            text: Markdown text.

        Returns:
            Safe HTML.
        """
        self.md.treeprocessors[_IdPrependingTreeprocessor.name].id_prefix = f"exec-{self.counter}--"
        self.counter += 1

        try:  # noqa: WPS501
            return Markup(self.md.convert(text))
        finally:
            self.md.treeprocessors[_IdPrependingTreeprocessor.name].id_prefix = ""


# provide a singleton
markdown = _MarkdownConverter()
