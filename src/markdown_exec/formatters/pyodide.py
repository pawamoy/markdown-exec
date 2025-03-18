"""Deprecated. Import from `markdown_exec` directly."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from markdown_exec._internal.formatters import pyodide


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Importing from `markdown_exec.formatters.pyodide` is deprecated. Import from `markdown_exec` directly.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(pyodide, name)
