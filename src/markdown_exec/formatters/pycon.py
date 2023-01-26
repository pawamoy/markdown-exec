"""Formatter for executing `pycon` code."""

from __future__ import annotations

import textwrap

from markupsafe import Markup

from markdown_exec.formatters.base import base_format
from markdown_exec.formatters.python import _run_python  # noqa: WPS450
from markdown_exec.logger import get_logger

logger = get_logger(__name__)


def _transform_source(code: str) -> tuple[str, str]:
    python_lines = []
    for line in code.split("\n"):
        if line.startswith(">>> "):
            python_lines.append(line[4:])
    python_code = "\n".join(python_lines)
    return python_code, textwrap.indent(python_code, ">>> ")


def _format_pycon(**kwargs) -> Markup:
    return base_format(language="pycon", run=_run_python, transform_source=_transform_source, **kwargs)
