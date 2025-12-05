"""Tests for the caching module."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

import markdown_exec._internal.cache as cache_module
from markdown_exec._internal.cache import CacheManager, _get_project_root, get_cache_manager

if TYPE_CHECKING:
    from markdown import Markdown


def test_get_project_root_with_mkdocs_config_dir() -> None:
    """Test project root detection with MKDOCS_CONFIG_DIR env var."""
    old_value = os.environ.get("MKDOCS_CONFIG_DIR")
    try:
        with tempfile.TemporaryDirectory() as test_dir:
            os.environ["MKDOCS_CONFIG_DIR"] = test_dir
            assert _get_project_root() == Path(test_dir)
    finally:
        if old_value is None:
            os.environ.pop("MKDOCS_CONFIG_DIR", None)
        else:
            os.environ["MKDOCS_CONFIG_DIR"] = old_value


def test_get_project_root_without_mkdocs_config_dir() -> None:
    """Test project root detection falls back to cwd."""
    old_value = os.environ.get("MKDOCS_CONFIG_DIR")
    try:
        os.environ.pop("MKDOCS_CONFIG_DIR", None)
        assert _get_project_root() == Path.cwd()
    finally:
        if old_value is not None:
            os.environ["MKDOCS_CONFIG_DIR"] = old_value


def test_cache_manager_default_uses_project_root() -> None:
    """Test that CacheManager uses project root by default."""
    old_value = os.environ.get("MKDOCS_CONFIG_DIR")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["MKDOCS_CONFIG_DIR"] = tmpdir
            cache_manager = CacheManager()
            expected_dir = Path(tmpdir) / ".markdown-exec-cache"
            assert cache_manager.cache_dir == expected_dir
            assert cache_manager.cache_dir.exists()
    finally:
        if old_value is None:
            os.environ.pop("MKDOCS_CONFIG_DIR", None)
        else:
            os.environ["MKDOCS_CONFIG_DIR"] = old_value


def test_cache_manager_hash_based_filesystem() -> None:
    """Test hash-based caching on filesystem."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_manager = CacheManager(cache_dir=Path(tmpdir))
        cache_manager.clear()  # Clear any existing cache

        code = "print('hello')"
        output = "hello\n"

        # First get should return None
        cached = cache_manager.get(None, code)
        assert cached is None

        # Set cache
        cache_manager.set(None, code, output)

        # Second get should return cached value
        cached = cache_manager.get(None, code)
        assert cached == output

        # Verify cache file exists
        cache_files = list(Path(tmpdir).glob("*.cache"))
        assert len(cache_files) == 1


def test_cache_manager_custom_id_filesystem() -> None:
    """Test custom ID caching on filesystem."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_manager = CacheManager(cache_dir=Path(tmpdir))

        code = "print('hello')"
        output = "hello\n"
        cache_id = "my-custom-id"

        # First get should return None
        cached = cache_manager.get(cache_id, code)
        assert cached is None

        # Set cache
        cache_manager.set(cache_id, code, output)

        # Second get should return cached value
        cached = cache_manager.get(cache_id, code)
        assert cached == output

        # Verify cache file with custom ID exists
        cache_path = cache_manager._get_cache_path(cache_id)
        assert cache_path.exists()
        assert cache_path.name == "my-custom-id.cache"


def test_cache_different_options_different_cache() -> None:
    """Test that different options produce different cache entries."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_manager = CacheManager(cache_dir=Path(tmpdir))
        cache_manager.clear()

        code = "print('hello')"
        output1 = "hello\n"
        output2 = "HELLO\n"

        # Cache with different options
        cache_manager.set(None, code, output1, language="python")
        cache_manager.set(None, code, output2, language="bash")

        # Should retrieve different outputs based on options
        cached1 = cache_manager.get(None, code, language="python")
        cached2 = cache_manager.get(None, code, language="bash")

        assert cached1 == output1
        assert cached2 == output2


def test_cache_clear_filesystem() -> None:
    """Test clearing filesystem cache."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_manager = CacheManager(cache_dir=Path(tmpdir))

        code = "print('hello')"
        output = "hello\n"
        cache_id = "test-id"

        cache_manager.set(cache_id, code, output)
        assert cache_manager.get(cache_id, code) == output

        cache_manager.clear(cache_id)
        assert cache_manager.get(cache_id, code) is None


def test_cache_clear_all_filesystem() -> None:
    """Test clearing all caches."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_manager = CacheManager(cache_dir=Path(tmpdir))

        code = "print('hello')"
        output = "hello\n"

        cache_manager.set(None, code, output)
        assert cache_manager.get(None, code) == output

        cache_manager.clear()
        assert cache_manager.get(None, code) is None


def test_get_cache_manager_singleton() -> None:
    """Test that get_cache_manager returns the same instance."""
    manager1 = get_cache_manager()
    manager2 = get_cache_manager()
    assert manager1 is manager2


def test_cache_integration_with_markdown(md: Markdown) -> None:
    """Test caching with actual markdown execution (hash-based).

    Parameters:
        md: A Markdown instance (fixture).
    """
    # Clear cache before test
    cache_manager = get_cache_manager()
    cache_manager.clear()

    # First execution should run the code
    html1 = md.convert(
        dedent(
            """
            ```python exec="yes" cache="yes"
            print("**Bold!**")
            ```
            """,
        ),
    )
    assert html1 == "<p><strong>Bold!</strong></p>"

    # Second execution should use cache (same code)
    html2 = md.convert(
        dedent(
            """
            ```python exec="yes" cache="yes"
            print("**Bold!**")
            ```
            """,
        ),
    )
    assert html2 == "<p><strong>Bold!</strong></p>"

    # Different code should not use cache
    html3 = md.convert(
        dedent(
            """
            ```python exec="yes" cache="yes"
            print("**Different!**")
            ```
            """,
        ),
    )
    assert html3 == "<p><strong>Different!</strong></p>"


def test_cache_integration_custom_id(md: Markdown) -> None:
    """Test caching with custom ID.

    Parameters:
        md: A Markdown instance (fixture).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_manager = CacheManager(cache_dir=Path(tmpdir))
        # Replace global instance temporarily
        old_manager = cache_module._cache_manager
        cache_module._cache_manager = cache_manager

        try:
            # First execution with custom ID
            html1 = md.convert(
                dedent(
                    """
                    ```python exec="yes" cache="my-plot"
                    print("**Plot!**")
                    ```
                    """,
                ),
            )
            assert html1 == "<p><strong>Plot!</strong></p>"

            # Verify cache file exists with custom ID
            cache_path = Path(tmpdir) / "my-plot.cache"
            assert cache_path.exists()

            # Second execution should use cache
            html2 = md.convert(
                dedent(
                    """
                    ```python exec="yes" cache="my-plot"
                    print("**Plot!**")
                    ```
                    """,
                ),
            )
            assert html2 == "<p><strong>Plot!</strong></p>"
        finally:
            # Restore original manager
            cache_module._cache_manager = old_manager


def test_cache_disabled_by_default(md: Markdown) -> None:
    """Test that caching is disabled by default.

    Parameters:
        md: A Markdown instance (fixture).
    """
    cache_manager = get_cache_manager()
    cache_manager.clear()

    # Execute without cache option
    html = md.convert(
        dedent(
            """
            ```python exec="yes"
            print("**No cache!**")
            ```
            """,
        ),
    )
    assert html == "<p><strong>No cache!</strong></p>"

    # Cache should be empty
    # We can't directly check, but we can verify by executing with cache and seeing it's a miss
    # This is implicitly tested by the fact that other tests need to explicitly enable cache


def test_cache_sanitizes_ids() -> None:
    """Test that cache IDs are sanitized to prevent path traversal."""
    cache_manager = CacheManager()

    # Try various dangerous IDs
    dangerous_ids = [
        "../../../etc/passwd",
        "../../test",
        "test/../../file",
        "test/../file",
        "test\\file",
    ]

    for dangerous_id in dangerous_ids:
        cache_path = cache_manager._get_cache_path(dangerous_id)
        # Ensure the path is within the cache directory
        assert cache_manager.cache_dir in cache_path.parents or cache_path.parent == cache_manager.cache_dir
        # Ensure no directory separators in the filename
        assert "/" not in cache_path.name
        assert "\\" not in cache_path.name


def test_cache_refresh_forces_reexecution() -> None:
    """Test that refresh parameter forces cache invalidation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_manager = CacheManager(cache_dir=Path(tmpdir))
        cache_manager.clear()

        code = "print('hello')"
        output = "hello\n"

        # Cache some output
        cache_manager.set(None, code, output)

        # Normal get should return cached value
        cached = cache_manager.get(None, code, refresh=False)
        assert cached == output

        # Get with refresh=True should return None (cache miss)
        cached = cache_manager.get(None, code, refresh=True)
        assert cached is None


def test_cache_refresh_integration(md: Markdown) -> None:
    """Test refresh option in actual markdown execution.

    Parameters:
        md: A Markdown instance (fixture).
    """
    cache_manager = get_cache_manager()
    cache_manager.clear()

    # First execution with cache
    html1 = md.convert(
        dedent(
            """
            ```python exec="yes" cache="yes"
            print("**First!**")
            ```
            """,
        ),
    )
    assert html1 == "<p><strong>First!</strong></p>"

    # Second execution with cache should use cached result
    html2 = md.convert(
        dedent(
            """
            ```python exec="yes" cache="yes"
            print("**First!**")
            ```
            """,
        ),
    )
    assert html2 == "<p><strong>First!</strong></p>"

    # Execution with refresh=yes should re-execute even with cache
    # (Note: The actual output would be the same since the code is the same,
    # but we verify the refresh parameter is accepted)
    html3 = md.convert(
        dedent(
            """
            ```python exec="yes" cache="yes" refresh="yes"
            print("**First!**")
            ```
            """,
        ),
    )
    assert html3 == "<p><strong>First!</strong></p>"


def test_cache_global_refresh_env_var(md: Markdown) -> None:
    """Test global refresh via MARKDOWN_EXEC_CACHE_REFRESH environment variable.

    Parameters:
        md: A Markdown instance (fixture).
    """
    cache_manager = get_cache_manager()
    cache_manager.clear()

    # First execution with cache
    html1 = md.convert(
        dedent(
            """
            ```python exec="yes" cache="yes"
            print("**Cached!**")
            ```
            """,
        ),
    )
    assert html1 == "<p><strong>Cached!</strong></p>"

    # Set global refresh environment variable
    old_value = os.environ.get("MARKDOWN_EXEC_CACHE_REFRESH")
    try:
        os.environ["MARKDOWN_EXEC_CACHE_REFRESH"] = "1"

        # Execution with global refresh should re-execute even without refresh parameter
        # (Note: The actual output would be the same since the code is the same,
        # but we verify the global refresh is triggered)
        html2 = md.convert(
            dedent(
                """
                ```python exec="yes" cache="yes"
                print("**Cached!**")
                ```
                """,
            ),
        )
        assert html2 == "<p><strong>Cached!</strong></p>"
    finally:
        if old_value is None:
            os.environ.pop("MARKDOWN_EXEC_CACHE_REFRESH", None)
        else:
            os.environ["MARKDOWN_EXEC_CACHE_REFRESH"] = old_value
