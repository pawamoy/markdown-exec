"""Formatter for executing shell code."""

from __future__ import annotations

import subprocess  # noqa: S404

from markdown_exec.formatters.base import base_format
from markdown_exec.rendering import code_block


def _run_sh(code: str, **extra: str) -> str:
    try:
        output = subprocess.check_output(["sh", "-c", code], stderr=subprocess.STDOUT).decode()  # noqa: S603,S607
    except subprocess.CalledProcessError as error:
        raise RuntimeError(code_block("sh", error.output, **extra))
    return output


def _format_sh(*args, **kwargs) -> str:
    return base_format("sh", _run_sh, *args, **kwargs)
