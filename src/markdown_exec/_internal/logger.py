# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2022, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from collections.abc import Callable


class _Logger:
    _default_logger: Any = logging.getLogger
    _instances: ClassVar[dict[str, _Logger]] = {}

    # See same code in Griffe project.
    def __init__(self, name: str) -> None:
        # Default logger that can be patched by third-party.
        self._logger = self.__class__._default_logger(name)

    def __getattr__(self, name: str) -> Any:
        # Forward everything to the logger.
        return getattr(self._logger, name)

    @classmethod
    def get(cls, name: str) -> _Logger:
        """Get a logger instance.

        Parameters:
            name: The logger name.

        Returns:
            The logger instance.
        """
        if name not in cls._instances:
            cls._instances[name] = cls(name)
        return cls._instances[name]

    @classmethod
    def _patch_loggers(cls, get_logger_func: Callable) -> None:
        # Patch current instances.
        for name, instance in cls._instances.items():
            instance._logger = get_logger_func(name)
        # Future instances will be patched as well.
        cls._default_logger = get_logger_func


def get_logger(name: str) -> _Logger:
    """Create and return a new logger instance.

    Parameters:
        name: The logger name.

    Returns:
        The logger.
    """
    return _Logger.get(name)


def patch_loggers(get_logger_func: Callable[[str], Any]) -> None:
    """Patch loggers.

    We provide the `patch_loggers`function so dependant libraries
    can patch loggers as they see fit.

    For example, to fit in the MkDocs logging configuration
    and prefix each log message with the module name:

    ```python
    import logging
    from markdown_exec.logger import patch_loggers


    class LoggerAdapter(logging.LoggerAdapter):
        def __init__(self, prefix, logger):
            super().__init__(logger, {})
            self.prefix = prefix

        def process(self, msg, kwargs):
            return f"{self.prefix}: {msg}", kwargs


    def get_logger(name):
        logger = logging.getLogger(f"mkdocs.plugins.{name}")
        return LoggerAdapter(name.split(".", 1)[0], logger)


    patch_loggers(get_logger)
    ```

    Parameters:
        get_logger_func: A function accepting a name as parameter and returning a logger.
    """
    _Logger._patch_loggers(get_logger_func)
