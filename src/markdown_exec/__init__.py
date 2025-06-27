"""Markdown Exec package.

Utilities to execute code blocks in Markdown files.
"""

from markdown_exec._internal.formatters.base import (
    ExecutionError,
    base_format,
    console_width,
    default_tabs,
    working_directory,
)
from markdown_exec._internal.logger import get_logger, patch_loggers
from markdown_exec._internal.main import MARKDOWN_EXEC_AUTO, formatter, formatters, validator
from markdown_exec._internal.processors import (
    HeadingReportingTreeprocessor,
    IdPrependingTreeprocessor,
    InsertHeadings,
    RemoveHeadings,
)
from markdown_exec._internal.rendering import (
    MarkdownConfig,
    MarkdownConverter,
    add_source,
    code_block,
    markdown_config,
    tabbed,
)

__all__ = [
    "MARKDOWN_EXEC_AUTO",
    "ExecutionError",
    "HeadingReportingTreeprocessor",
    "IdPrependingTreeprocessor",
    "InsertHeadings",
    "MarkdownConfig",
    "MarkdownConverter",
    "RemoveHeadings",
    "add_source",
    "base_format",
    "code_block",
    "console_width",
    "default_tabs",
    "formatter",
    "formatters",
    "get_logger",
    "markdown_config",
    "patch_loggers",
    "tabbed",
    "validator",
    "working_directory",
]


try:
    from markdown_exec._internal.mkdocs_plugin import MarkdownExecPlugin, MarkdownExecPluginConfig
except ImportError:
    pass
else:
    __all__ += [
        "MarkdownExecPlugin",
        "MarkdownExecPluginConfig",
    ]
