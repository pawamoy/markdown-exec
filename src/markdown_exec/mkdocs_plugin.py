"""This module contains an optional plugin for MkDocs."""

from mkdocs.config import Config, config_options
from mkdocs.plugins import BasePlugin

from markdown_exec import formatter, validator


class MarkdownExecPlugin(BasePlugin):
    """MkDocs plugin to easily enable custom fences for code blocks execution."""

    config_scheme = (("languages", config_options.Type(list, default=["py", "python", "pycon", "md", "markdown"])),)

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
