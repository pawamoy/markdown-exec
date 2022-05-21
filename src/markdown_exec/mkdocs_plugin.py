"""This module contains an optional plugin for MkDocs."""

import logging

from mkdocs.config import Config, config_options
from mkdocs.plugins import BasePlugin

from markdown_exec import formatter, formatters, validator
from markdown_exec.logger import patch_loggers


class _LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, prefix, logger):
        super().__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return f"{self.prefix}: {msg}", kwargs


def _get_logger(name):
    logger = logging.getLogger(f"mkdocs.plugins.{name}")
    return _LoggerAdapter(name.split(".", 1)[0], logger)


patch_loggers(_get_logger)


class MarkdownExecPlugin(BasePlugin):
    """MkDocs plugin to easily enable custom fences for code blocks execution."""

    config_scheme = (("languages", config_options.Type(list, default=list(formatters.keys()))),)

    def on_config(self, config: Config, **kwargs) -> Config:  # noqa: D102
        self.languages = self.config["languages"]

        mdx_configs = config.setdefault("mdx_configs", {})
        superfences = mdx_configs.setdefault("pymdownx.superfences", {})
        custom_fences = superfences.setdefault("custom_fences", [])
        for language in self.languages:
            custom_fences.append(
                {
                    "name": language,
                    "class": language,
                    "validator": validator,
                    "format": formatter,
                }
            )
        return config
