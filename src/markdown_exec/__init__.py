"""
Markdown Exec package.

Utilities to execute code blocks in Markdown files.
"""

# https://facelessuser.github.io/pymdown-extensions/extensions/superfences/#custom-fences
# https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown-extensions/#snippets

from __future__ import annotations

from typing import Any

from markdown import Markdown

from markdown_exec.python import exec_python

__all__: list[str] = ["formatter", "validator"]  # noqa: WPS410


_formatters = {
    "python": exec_python,
}


def validator(
    language: str, inputs: dict[str, str], options: dict[str, Any], attrs: dict[str, Any], md: Markdown
) -> bool:
    """Validate code blocks inputs.

    Parameters:
        language: The code language, like python or bash.
        inputs: The code block inputs, to be sorted into options and attrs.
        options: The container for options.
        attrs: The container for attrs:
        md: The Markdown instance.

    Returns:
        Success or not.
    """
    exec_value = _to_bool(inputs.pop("exec", "no"))
    if not exec_value:
        return False
    isolate_value = _to_bool(inputs.pop("isolate", "no"))
    show_source_value = inputs.pop("show_source", "")
    options["exec"] = exec_value
    options["isolate"] = isolate_value
    options["show_source"] = show_source_value
    return True


def formatter(
    source: str,
    language: str,
    css_class: str,
    options: dict[str, Any],
    md: Markdown,
    classes: list[str] | None = None,
    id_value: str = "",
    attrs: dict[str, Any] | None = None,
    **kwargs: Any,
) -> str:
    """Execute code and return HTML.

    Parameters:
        source: The code to execute.
        language: The code language, like python or bash.
        css_class: The CSS class to add to the HTML element.
        options: The container for options.
        attrs: The container for attrs:
        md: The Markdown instance.
        classes: Additional CSS classes.
        id_value: An optional HTML id.
        attrs: Additional attributes
        **kwargs: Additional arguments passed to SuperFences default formatters.

    Returns:
        HTML contents.
    """
    fmt = _formatters.get(language, lambda source, *args, **kwargs: source)
    return fmt(source, md, **options)


falsy_values = {"", "no", "off", "false", "0"}
truthy_values = {"yes", "on", "true", "1"}


def _to_bool(value: str) -> bool:
    return value.lower() not in falsy_values


def _to_bool_or_value(value: str) -> bool | str:
    if value.lower() in falsy_values:
        return False
    if value.lower() in truthy_values:
        return True
    return value
