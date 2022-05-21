"""Configuration for the pytest test suite."""

import pytest
from markdown import Markdown

from markdown_exec import formatter, formatters, validator


@pytest.fixture()
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
        for language in formatters.keys()
    ]
    return Markdown(
        extensions=["pymdownx.superfences"],
        extension_configs={"pymdownx.superfences": {"custom_fences": fences}},
    )
