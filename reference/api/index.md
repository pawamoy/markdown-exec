# markdown_exec

Markdown Exec package.

Utilities to execute code blocks in Markdown files.

Modules:

- **`formatters`** – Deprecated. Import from markdown_exec directly.
- **`logger`** – Deprecated. Import from markdown_exec directly.
- **`mkdocs_plugin`** – Deprecated. Import from markdown_exec directly.
- **`processors`** – Deprecated. Import from markdown_exec directly.
- **`rendering`** – Deprecated. Import from markdown_exec directly.

Classes:

- **`ExecutionError`** – Exception raised for errors during execution of a code block.
- **`HeadingReportingTreeprocessor`** – Records the heading elements encountered in the document.
- **`IdPrependingTreeprocessor`** – Prepend the configured prefix to IDs of all HTML elements.
- **`InsertHeadings`** – Our headings insertor.
- **`MarkdownConfig`** – This class returns a singleton used to store Markdown extensions configuration.
- **`MarkdownConverter`** – Helper class to avoid breaking the original Markdown instance state.
- **`MarkdownExecPlugin`** – MkDocs plugin to easily enable custom fences for code blocks execution.
- **`MarkdownExecPluginConfig`** – Configuration of the plugin (for mkdocs.yml).
- **`RemoveHeadings`** – Our headings remover.

Functions:

- **`add_source`** – Add source code block to the output.
- **`base_format`** – Execute code and return HTML.
- **`code_block`** – Format code as a code block.
- **`console_width`** – Set the console width for the duration of the context.
- **`formatter`** – Execute code and return HTML.
- **`get_logger`** – Create and return a new logger instance.
- **`patch_loggers`** – Patch loggers.
- **`tabbed`** – Format tabs using pymdownx.tabbed extension.
- **`validator`** – Validate code blocks inputs.
- **`working_directory`** – Change the working directory for the duration of the context.

Attributes:

- **`MARKDOWN_EXEC_AUTO`** – Languages to automatically execute.
- **`default_tabs`** – Default tab titles.
- **`markdown_config`** – This object can be used to save the configuration of your Markdown extensions.

## MARKDOWN_EXEC_AUTO

```
MARKDOWN_EXEC_AUTO = [strip() for lang in split(',')]

```

Languages to automatically execute.

## default_tabs

```
default_tabs = ('Source', 'Result')

```

Default tab titles.

## markdown_config

```
markdown_config = MarkdownConfig()

```

This object can be used to save the configuration of your Markdown extensions.

For example, since we provide a MkDocs plugin, we use it to store the configuration that was read from `mkdocs.yml`:

```
from markdown_exec.rendering import markdown_config

# ...in relevant events/hooks, access and modify extensions and their configs, then:
markdown_config.save(extensions, extensions_config)

```

See the actual event hook: on_config. See the save and reset methods.

Without it, Markdown Exec will rely on the `registeredExtensions` attribute of the original Markdown instance, which does not forward everything that was configured, notably extensions like `tables`. Other extensions such as `attr_list` are visible, but fail to register properly when reusing their instances. It means that the rendered HTML might differ from what you expect (tables not rendered, attribute lists not injected, emojis not working, etc.).

## ExecutionError

```
ExecutionError(message: str, returncode: int | None = None)

```

Bases: `Exception`

Exception raised for errors during execution of a code block.

Attributes:

- **`message`** – The exception message.
- **`returncode`** – The code returned by the execution of the code block.

### returncode

```
returncode = returncode

```

The code returned by the execution of the code block.

## HeadingReportingTreeprocessor

```
HeadingReportingTreeprocessor(
    md: Markdown, headings: list[Element]
)

```

Bases: `Treeprocessor`

Records the heading elements encountered in the document.

Methods:

- **`run`** – Run the treeprocessor.

Attributes:

- **`headings`** – The list of heading elements.
- **`name`** – The name of the treeprocessor.
- **`regex`** – The regex to match heading tags.

### headings

```
headings = headings

```

The list of heading elements.

### name

```
name = 'markdown_exec_record_headings'

```

The name of the treeprocessor.

### regex

```
regex = compile('[Hh][1-6]')

```

The regex to match heading tags.

### run

```
run(root: Element) -> None

```

Run the treeprocessor.

## IdPrependingTreeprocessor

```
IdPrependingTreeprocessor(md: Markdown, id_prefix: str)

```

Bases: `Treeprocessor`

Prepend the configured prefix to IDs of all HTML elements.

Methods:

- **`run`** – Run the treeprocessor.

Attributes:

- **`id_prefix`** – The prefix to prepend to IDs.
- **`name`** – The name of the treeprocessor.

### id_prefix

```
id_prefix = id_prefix

```

The prefix to prepend to IDs.

### name

```
name = 'markdown_exec_ids'

```

The name of the treeprocessor.

### run

```
run(root: Element) -> None

```

Run the treeprocessor.

## InsertHeadings

```
InsertHeadings(md: Markdown)

```

Bases: `Treeprocessor`

Our headings insertor.

Parameters:

- **`md`** (`Markdown`) – A markdown.Markdown instance.

Methods:

- **`run`** – Run the treeprocessor.

Attributes:

- **`headings`** (`dict[Markup, list[Element]]`) – The dictionary of headings.
- **`name`** – The name of the treeprocessor.

### headings

```
headings: dict[Markup, list[Element]] = {}

```

The dictionary of headings.

### name

```
name = 'markdown_exec_insert_headings'

```

The name of the treeprocessor.

### run

```
run(root: Element) -> None

```

Run the treeprocessor.

## MarkdownConfig

```
MarkdownConfig()

```

This class returns a singleton used to store Markdown extensions configuration.

You don't have to instantiate the singleton yourself: we provide it as markdown_config.

Methods:

- **`__new__`** – Return the singleton instance.
- **`reset`** – Reset Markdown extensions and their configuration.
- **`save`** – Save Markdown extensions and their configuration.

Attributes:

- **`exts`** (`list[str] | None`) – The Markdown extensions.
- **`exts_config`** (`dict[str, dict[str, Any]] | None`) – The extensions configuration.

### exts

```
exts: list[str] | None = None

```

The Markdown extensions.

### exts_config

```
exts_config: dict[str, dict[str, Any]] | None = None

```

The extensions configuration.

### __new__

```
__new__() -> MarkdownConfig

```

Return the singleton instance.

### reset

```
reset() -> None

```

Reset Markdown extensions and their configuration.

### save

```
save(
    exts: list[str], exts_config: dict[str, dict[str, Any]]
) -> None

```

Save Markdown extensions and their configuration.

Parameters:

- **`exts`** (`list[str]`) – The Markdown extensions.
- **`exts_config`** (`dict[str, dict[str, Any]]`) – The extensions configuration.

## MarkdownConverter

```
MarkdownConverter(md: Markdown, *, update_toc: bool = True)

```

Helper class to avoid breaking the original Markdown instance state.

Methods:

- **`convert`** – Convert Markdown text to safe HTML.

Attributes:

- **`counter`** (`int`) – A counter to generate unique IDs for code blocks.

### counter

```
counter: int = 0

```

A counter to generate unique IDs for code blocks.

### convert

```
convert(
    text: str,
    stash: dict[str, str] | None = None,
    id_prefix: str | None = None,
) -> Markup

```

Convert Markdown text to safe HTML.

Parameters:

- **`text`** (`str`) – Markdown text.
- **`stash`** (`dict[str, str] | None`, default: `None` ) – An HTML stash.

Returns:

- `Markup` – Safe HTML.

## MarkdownExecPlugin

Bases: `BasePlugin[MarkdownExecPluginConfig]`

MkDocs plugin to easily enable custom fences for code blocks execution.

Methods:

- **`on_config`** – Configure the plugin.
- **`on_env`** – Add assets to the environment.
- **`on_post_build`** – Reset the plugin state.

### on_config

```
on_config(config: MkDocsConfig) -> MkDocsConfig | None

```

Configure the plugin.

Hook for the [`on_config` event](https://www.mkdocs.org/user-guide/plugins/#on_config). In this hook, we add custom fences for all the supported languages.

We also save the Markdown extensions configuration into markdown_config.

Parameters:

- **`config`** (`MkDocsConfig`) – The MkDocs config object.

Returns:

- `MkDocsConfig | None` – The modified config.

### on_env

```
on_env(
    env: Environment, *, config: MkDocsConfig, files: Files
) -> Environment | None

```

Add assets to the environment.

### on_post_build

```
on_post_build(*, config: MkDocsConfig) -> None

```

Reset the plugin state.

## MarkdownExecPluginConfig

Bases: `Config`

Configuration of the plugin (for `mkdocs.yml`).

Attributes:

- **`ansi`** – Whether the ansi extra is required when installing the package.
- **`languages`** – Which languages to enabled the extension for.

### ansi

```
ansi = Choice(
    ("auto", "off", "required", True, False), default="auto"
)

```

Whether the `ansi` extra is required when installing the package.

### languages

```
languages = ListOfItems(
    Choice(keys()), default=list(keys())
)

```

Which languages to enabled the extension for.

## RemoveHeadings

Bases: `Treeprocessor`

Our headings remover.

Methods:

- **`run`** – Run the treeprocessor.

Attributes:

- **`name`** – The name of the treeprocessor.

### name

```
name = 'markdown_exec_remove_headings'

```

The name of the treeprocessor.

### run

```
run(root: Element) -> None

```

Run the treeprocessor.

## add_source

```
add_source(
    *,
    source: str,
    location: str,
    output: str,
    language: str,
    tabs: tuple[str, str],
    result: str = "",
    **extra: str,
) -> str

```

Add source code block to the output.

Parameters:

- **`source`** (`str`) – The source code block.
- **`location`** (`str`) – Where to add the source (above, below, tabbed-left, tabbed-right, console).
- **`output`** (`str`) – The current output.
- **`language`** (`str`) – The code language.
- **`tabs`** (`tuple[str, str]`) – Tabs titles (if used).
- **`result`** (`str`, default: `''` ) – Syntax to use when concatenating source and result with "console" location.
- **`**extra`** (`str`, default: `{}` ) – Extra options added back to source code block.

Raises:

- `ValueError` – When the given location is not supported.

Returns:

- `str` – The updated output.

## base_format

```
base_format(
    *,
    language: str,
    run: Callable,
    code: str,
    md: Markdown,
    html: bool = False,
    source: str = "",
    result: str = "",
    tabs: tuple[str, str] = default_tabs,
    id: str = "",
    id_prefix: str | None = None,
    returncode: int = 0,
    transform_source: Callable[[str], tuple[str, str]]
    | None = None,
    session: str | None = None,
    update_toc: bool = True,
    workdir: str | None = None,
    width: int | None = None,
    **options: Any,
) -> Markup

```

Execute code and return HTML.

Parameters:

- **`language`** (`str`) – The code language.
- **`run`** (`Callable`) – Function that runs code and returns output.
- **`code`** (`str`) – The code to execute.
- **`md`** (`Markdown`) – The Markdown instance.
- **`html`** (`bool`, default: `False` ) – Whether to inject output as HTML directly, without rendering.
- **`source`** (`str`, default: `''` ) – Whether to show source as well, and where.
- **`result`** (`str`, default: `''` ) – If provided, use as language to format result in a code block.
- **`tabs`** (`tuple[str, str]`, default: `default_tabs` ) – Titles of tabs (if used).
- **`id`** (`str`, default: `''` ) – An optional ID for the code block (useful when warning about errors).
- **`id_prefix`** (`str | None`, default: `None` ) – A string used to prefix HTML ids in the generated HTML.
- **`returncode`** (`int`, default: `0` ) – The expected exit code.
- **`transform_source`** (`Callable[[str], tuple[str, str]] | None`, default: `None` ) – An optional callable that returns transformed versions of the source. The input source is the one that is ran, the output source is the one that is rendered (when the source option is enabled).
- **`session`** (`str | None`, default: `None` ) – A session name, to persist state between executed code blocks.
- **`update_toc`** (`bool`, default: `True` ) – Whether to include generated headings into the Markdown table of contents (toc extension).
- **`workdir`** (`str | None`, default: `None` ) – The working directory to use for the execution.
- **`**options`** (`Any`, default: `{}` ) – Additional options passed from the formatter.

Returns:

- `Markup` – HTML contents.

## code_block

```
code_block(language: str, code: str, **options: str) -> str

```

Format code as a code block.

Parameters:

- **`language`** (`str`) – The code block language.
- **`code`** (`str`) – The source code to format.
- **`**options`** (`str`, default: `{}` ) – Additional options passed from the source, to add back to the generated code block.

Returns:

- `str` – The formatted code block.

## console_width

```
console_width(width: int | None = None) -> Iterator[None]

```

Set the console width for the duration of the context.

The console width is set using the `COLUMNS` environment variable.

Parameters:

- **`width`** (`int | None`, default: `None` ) – The width to set the console to.

## formatter

```
formatter(
    source: str,
    language: str,
    css_class: str,
    options: dict[str, Any],
    md: Markdown,
    classes: list[str] | None = None,
    id_value: str = "",
    attrs: dict[str, Any] | None = None,
    **kwargs: Any,
) -> str

```

Execute code and return HTML.

Parameters:

- **`source`** (`str`) – The code to execute.
- **`language`** (`str`) – The code language, like python or bash.
- **`css_class`** (`str`) – The CSS class to add to the HTML element.
- **`options`** (`dict[str, Any]`) – The container for options.
- **`attrs`** (`dict[str, Any] | None`, default: `None` ) – The container for attrs:
- **`md`** (`Markdown`) – The Markdown instance.
- **`classes`** (`list[str] | None`, default: `None` ) – Additional CSS classes.
- **`id_value`** (`str`, default: `''` ) – An optional HTML id.
- **`attrs`** (`dict[str, Any] | None`, default: `None` ) – Additional attributes
- **`**kwargs`** (`Any`, default: `{}` ) – Additional arguments passed to SuperFences default formatters.

Returns:

- `str` – HTML contents.

## get_logger

```
get_logger(name: str) -> _Logger

```

Create and return a new logger instance.

Parameters:

- **`name`** (`str`) – The logger name.

Returns:

- `_Logger` – The logger.

## patch_loggers

```
patch_loggers(
    get_logger_func: Callable[[str], Any],
) -> None

```

Patch loggers.

We provide the `patch_loggers`function so dependant libraries can patch loggers as they see fit.

For example, to fit in the MkDocs logging configuration and prefix each log message with the module name:

```
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

- **`get_logger_func`** (`Callable[[str], Any]`) – A function accepting a name as parameter and returning a logger.

## tabbed

```
tabbed(*tabs: tuple[str, str]) -> str

```

Format tabs using `pymdownx.tabbed` extension.

Parameters:

- **`*tabs`** (`tuple[str, str]`, default: `()` ) – Tuples of strings: title and text.

Returns:

- `str` – The formatted tabs.

## validator

```
validator(
    language: str,
    inputs: dict[str, str],
    options: dict[str, Any],
    attrs: dict[str, Any],
    md: Markdown,
) -> bool

```

Validate code blocks inputs.

Parameters:

- **`language`** (`str`) – The code language, like python or bash.
- **`inputs`** (`dict[str, str]`) – The code block inputs, to be sorted into options and attrs.
- **`options`** (`dict[str, Any]`) – The container for options.
- **`attrs`** (`dict[str, Any]`) – The container for attrs:
- **`md`** (`Markdown`) – The Markdown instance.

Returns:

- `bool` – Success or not.

## working_directory

```
working_directory(
    path: str | None = None,
) -> Iterator[None]

```

Change the working directory for the duration of the context.

Parameters:

- **`path`** (`str | None`, default: `None` ) – The path to change the working directory to.

## formatters

Deprecated. Import from `markdown_exec` directly.

Modules:

- **`base`** – Deprecated. Import from markdown_exec directly.
- **`bash`** – Deprecated. Import from markdown_exec directly.
- **`console`** – Deprecated. Import from markdown_exec directly.
- **`markdown`** – Deprecated. Import from markdown_exec directly.
- **`pycon`** – Deprecated. Import from markdown_exec directly.
- **`pyodide`** – Deprecated. Import from markdown_exec directly.
- **`python`** – Deprecated. Import from markdown_exec directly.
- **`sh`** – Deprecated. Import from markdown_exec directly.
- **`tree`** – Deprecated. Import from markdown_exec directly.

### base

Deprecated. Import from `markdown_exec` directly.

### bash

Deprecated. Import from `markdown_exec` directly.

### console

Deprecated. Import from `markdown_exec` directly.

### markdown

Deprecated. Import from `markdown_exec` directly.

### pycon

Deprecated. Import from `markdown_exec` directly.

### pyodide

Deprecated. Import from `markdown_exec` directly.

### python

Deprecated. Import from `markdown_exec` directly.

### sh

Deprecated. Import from `markdown_exec` directly.

### tree

Deprecated. Import from `markdown_exec` directly.

## logger

Deprecated. Import from `markdown_exec` directly.

## mkdocs_plugin

Deprecated. Import from `markdown_exec` directly.

## processors

Deprecated. Import from `markdown_exec` directly.

## rendering

Deprecated. Import from `markdown_exec` directly.
