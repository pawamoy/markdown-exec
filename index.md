# Markdown Exec

Utilities to execute code blocks in Markdown files.

For example, you write a Python code block that computes some HTML, and this HTML is injected in place of the code block.

## Installation

```
pip install "markdown-exec[ansi]"
```

The `ansi` extra provides the necessary bits (`pygments-ansi-color` and a CSS file) to render ANSI colors in HTML code blocks. The CSS file is automatically added to MkDocs' `extra_css` when Markdown Exec is activated via `plugins` (see below).

## Configuration

This extension relies on the [SuperFences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/) extension of [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/).

To allow execution of code blocks, configure a custom fence from Python:

```
from markdown import Markdown
from markdown_exec import formatter, validator

Markdown(
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
                # ...one fence for each language we support:
                # bash, console, md, markdown, py, python, pycon, pyodide, sh, tree, etc.
            ]
        }
    }
)
```

...or in MkDocs configuration file, as a Markdown extension:

```
# mkdocs.yml
markdown_extensions:
- pymdownx.superfences:
    custom_fences:
    - name: python
      class: python
      validator: !!python/name:markdown_exec.validator
      format: !!python/name:markdown_exec.formatter
    # ...one fence for each language we support:
    # bash, console, md, markdown, py, python, pycon, sh, tree
```

...or in MkDocs configuration file, as a plugin:

```
# mkdocs.yml
plugins:
- search
- markdown-exec

# SuperFences must still be enabled!
markdown_extensions:
- pymdownx.superfences
```

Tip

We recommend enabling Markdown Exec with the MkDocs plugin if you are using MkDocs: it will take care of adding relevant assets (CSS/JS) to the final site when needed.

Limitation of configuration through Markdown/PyMDown.

Configuration through `pymdownx.superfences` directly is not well supported for fences that require assets inclusion, like `pyodide`. For these you will have to include the assets manually. In the future we will provide ways to include them automatically.

## Usage

You are now able to execute code blocks instead of displaying them:

````
```python exec="on"
print("Hello Markdown!")
````

```

The `exec` option will be true for every possible value except `0`, `no`, `off` and `false` (case insensitive).

Below you can see an example of running a bash script that is expected to
return a non-zero exit code:

```

```bash exec="1" source="tabbed-left" returncode="2"
grep extra_css README.md && exit 2
```

````

See [usage](https://pawamoy.github.io/markdown-exec/usage/) for more details,
and the [gallery](https://pawamoy.github.io/markdown-exec/gallery/) for more examples!

## Sponsors

**Silver sponsors**

**Bronze sponsors**

---

*And 8 more private sponsor(s).*```
````
