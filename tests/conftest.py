"""Configuration for the pytest test suite."""

import shutil
import tempfile
from collections.abc import Generator

import pytest
from markdown import Markdown

from markdown_exec import formatter, formatters, validator
from markdown_exec._internal import cache as cache_module


@pytest.fixture(autouse=True)
def _isolate_cache(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Isolate cache directory for each test.

    This ensures tests use a temporary cache directory that is
    cleaned up after each test, preventing cache pollution between tests.
    """
    # Create a temporary directory for cache
    tmpdir = tempfile.mkdtemp(prefix="markdown-exec-test-cache-")

    # Set MKDOCS_CONFIG_DIR to point to the temp directory
    monkeypatch.setenv("MKDOCS_CONFIG_DIR", tmpdir)

    # Reset the global cache manager to pick up the new directory
    cache_module._cache_manager = None

    yield

    # Clean up the temporary cache directory
    shutil.rmtree(tmpdir, ignore_errors=True)

    # Reset the cache manager again
    cache_module._cache_manager = None


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
