"""Formatter for executing shell code."""

from __future__ import annotations

import subprocess  # noqa: S404

from markdown_exec.formatters.base import ExecutionError, base_format
from markdown_exec.rendering import code_block


def _run_bash(code: str, *, returncode: int = 0, **extra: str) -> str:
    process = subprocess.run(  # noqa: S603,S607
        ["bash", "-c", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if process.returncode != returncode:
        raise ExecutionError(code_block("sh", process.stdout, **extra), process.returncode)
    return process.stdout


def _format_bash(**kwargs) -> str:
    return base_format(language="bash", run=_run_bash, **kwargs)
