# Formatter for executing shell console code.

from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING, Any

from markdown_exec._internal.formatters.base import base_format
from markdown_exec._internal.formatters.sh import _run_sh
from markdown_exec._internal.logger import get_logger

if TYPE_CHECKING:
    from markupsafe import Markup

_logger = get_logger(__name__)


def _transform_source(code: str) -> tuple[str, str]:
    sh_lines = []
    for line in code.split("\n"):
        prompt = line[:2]
        if prompt in {"$ ", "% "}:
            sh_lines.append(line[2:])
    sh_code = "\n".join(sh_lines)
    return sh_code, textwrap.indent(sh_code, prompt)


def _format_console(**kwargs: Any) -> Markup:
    return base_format(language="console", run=_run_sh, transform_source=_transform_source, **kwargs)
