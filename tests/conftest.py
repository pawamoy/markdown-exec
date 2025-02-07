"""Configuration for the pytest test suite."""

from collections.abc import Iterable

import pytest
from markdown import Markdown

from markdown_exec import formatter, formatters, validator
from markdown_exec.formatters.jupyter import _shutdown_kernels


@pytest.fixture
def md() -> Markdown:
    """Return a Markdown instance.

    Returns:
        Markdown instance.
    """
    fences = [
        {
            "name": language,
            "class": language,
            "validator": validator,
            "format": formatter,
        }
        for language in formatters
    ]
    return Markdown(
        extensions=["pymdownx.superfences", "pymdownx.tabbed"],
        extension_configs={"pymdownx.superfences": {"custom_fences": fences}},
    )

@pytest.fixture(autouse=True)
def cleanup() -> Iterable[None]:
    """Cleanup the test environment."""
    yield
    _shutdown_kernels()
