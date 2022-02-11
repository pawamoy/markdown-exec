"""Configuration for the pytest test suite."""

import pytest
from markdown import Markdown

from markdown_exec import formatter, validator


@pytest.fixture()
def md() -> Markdown:
    """Return a Markdown instance.

    Returns:
        Markdown instance.
    """
    return Markdown(
        extensions=["pymdownx.superfences"],
        extension_configs={
            "pymdownx.superfences": {
                "custom_fences": [
                    {
                        "name": "python",
                        "class": "python",
                        "validator": validator,
                        "format": formatter,
                    }
                ]
            }
        },
    )
