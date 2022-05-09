"""Formatter for literate Markdown."""

from __future__ import annotations

from markdown_exec.formatters.base import base_format


def _format_markdown(*args, **kwargs) -> str:
    return base_format("md", lambda code, **_: code, *args, **kwargs)
