"""Formatter for executing `tscon` code."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from markdown_exec.formatters.base import base_format
from markdown_exec.formatters.typescript import _run_typescript
from markdown_exec.logger import get_logger

if TYPE_CHECKING:
    from markupsafe import Markup

logger = get_logger(__name__)


def _transform_source(code: str) -> tuple[str, str]:
    typescript_lines = []
    tscon_lines = []
    for line in code.split("\n"):
        if line.startswith("> "):
            tscon_lines.append(line)
            typescript_lines.append(line[2:])
        elif line.startswith("... "):
            tscon_lines.append(line)
            typescript_lines.append(line[4:])
    typescript_code = "\n".join(typescript_lines)
    return typescript_code, "\n".join(tscon_lines)


def _format_tscon(**kwargs: Any) -> Markup:
    return base_format(
        language="tscon",
        run=_run_typescript,
        transform_source=_transform_source,
        **kwargs,
    )
