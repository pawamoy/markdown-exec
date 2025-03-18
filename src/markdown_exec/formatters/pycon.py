"""Deprecated. Import from `markdown_exec` directly."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from markdown_exec._internal.formatters import pycon


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Importing from `markdown_exec.formatters.pycon` is deprecated. Import from `markdown_exec` directly.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(pycon, name)
