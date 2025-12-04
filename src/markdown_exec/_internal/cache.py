from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from markdown_exec._internal.logger import get_logger

_logger = get_logger(__name__)


def _get_project_root() -> Path:
    """Determine the project root directory.

    Uses MKDOCS_CONFIG_DIR if available (set by MkDocs plugin),
    otherwise falls back to current working directory.

    Returns:
        Path to the project root directory.
    """
    mkdocs_config_dir = os.getenv("MKDOCS_CONFIG_DIR")
    if mkdocs_config_dir:
        return Path(mkdocs_config_dir)
    return Path.cwd()


class CacheManager:
    """Manager for code execution caching.

    Provides filesystem-based caching for cross-build persistence.
    """

    def __init__(self, cache_dir: Path | None = None) -> None:
        """Initialize the cache manager.

        Parameters:
            cache_dir: Directory for filesystem cache. If None, uses .markdown-exec-cache
                      in the project root directory.
        """
        if cache_dir is None:
            cache_dir = _get_project_root() / ".markdown-exec-cache"
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _compute_hash(self, code: str, **options: Any) -> str:
        """Compute a hash for the given code and options.

        Parameters:
            code: The source code to hash.
            **options: Additional options that affect execution (language, html, etc.).

        Returns:
            A hex digest hash string.
        """
        # Create a deterministic string from code and relevant options
        # Exclude options that don't affect the output (like 'source', 'tabs', 'id', 'id_prefix')
        relevant_options = {
            k: v for k, v in sorted(options.items()) if k not in {"source", "tabs", "id", "id_prefix", "cache", "extra"}
        }

        # Include 'extra' options that might affect execution
        if "extra" in options and isinstance(options["extra"], dict):
            relevant_options["extra"] = dict(sorted(options["extra"].items()))

        cache_key = json.dumps(
            {"code": code, "options": relevant_options},
            sort_keys=True,
            default=str,
        )
        return hashlib.sha256(cache_key.encode()).hexdigest()

    def _get_cache_path(self, cache_id: str) -> Path:
        """Get the filesystem path for a cache entry.

        Parameters:
            cache_id: The cache identifier (hash or custom ID).

        Returns:
            Path to the cache file.
        """
        # Sanitize the cache_id to prevent path traversal
        safe_id = "".join(c if c.isalnum() or c in "-_" else "_" for c in cache_id)
        return self.cache_dir / f"{safe_id}.cache"

    def get(
        self,
        cache_id: str | None,
        code: str,
        refresh: bool = False,  # noqa: FBT001, FBT002
        **options: Any,
    ) -> str | None:
        """Retrieve cached output for the given code.

        Parameters:
            cache_id: Custom cache identifier, or None to use hash-based caching.
            code: The source code.
            refresh: If True, ignore cache and force re-execution.
            **options: Execution options used for hash computation.

        Returns:
            Cached output string, or None if not found or refresh is True.
        """
        # Force cache miss if refresh is requested
        if refresh:
            _logger.debug("Cache refresh requested, forcing re-execution")
            return None

        # Determine the cache key
        cache_key = self._compute_hash(code, **options) if cache_id is None else cache_id

        # Check filesystem cache
        cache_path = self._get_cache_path(cache_key)
        if cache_path.exists():
            try:
                output = cache_path.read_text(encoding="utf-8")
            except OSError as error:
                _logger.warning("Failed to read cache file %s: %s", cache_path, error)
            else:
                _logger.debug("Cache hit: %s", cache_key)
                return output

        _logger.debug("Cache miss: %s", cache_key)
        return None

    def set(
        self,
        cache_id: str | None,
        code: str,
        output: str,
        **options: Any,
    ) -> None:
        """Store output in cache for the given code.

        Parameters:
            cache_id: Custom cache identifier, or None to use hash-based caching.
            code: The source code.
            output: The execution output to cache.
            **options: Execution options used for hash computation.
        """
        # Determine the cache key
        cache_key = self._compute_hash(code, **options) if cache_id is None else cache_id

        # Write to filesystem cache
        cache_path = self._get_cache_path(cache_key)
        try:
            cache_path.write_text(output, encoding="utf-8")
            _logger.debug("Cached to filesystem: %s (%s)", cache_key, cache_path)
        except OSError as error:
            _logger.warning("Failed to write cache file %s: %s", cache_path, error)

    def clear(self, cache_id: str | None = None) -> None:
        """Clear the filesystem cache.

        Parameters:
            cache_id: Specific cache ID to clear, or None to clear all.
        """
        if cache_id is None:
            # Clear all cache files
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    cache_file.unlink()
                    _logger.debug("Deleted cache file: %s", cache_file)
                except OSError as error:
                    _logger.warning("Failed to delete cache file %s: %s", cache_file, error)
        else:
            # Clear specific cache file
            cache_path = self._get_cache_path(cache_id)
            if cache_path.exists():
                try:
                    cache_path.unlink()
                    _logger.debug("Deleted cache file: %s", cache_path)
                except OSError as error:
                    _logger.warning("Failed to delete cache file %s: %s", cache_path, error)


# Global cache manager instance
_cache_manager: CacheManager | None = None


def get_cache_manager() -> CacheManager:
    """Get or create the global cache manager instance.

    Returns:
        The global CacheManager instance.
    """
    global _cache_manager  # noqa: PLW0603
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager
