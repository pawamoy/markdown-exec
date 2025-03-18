"""Deprecated. Import from `markdown_exec` directly."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from markdown_exec._internal import rendering


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Importing from `markdown_exec.rendering` is deprecated. Import from `markdown_exec` directly.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(rendering, name)
