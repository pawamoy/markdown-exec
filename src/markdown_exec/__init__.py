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
