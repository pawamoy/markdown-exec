# Markdown Exec

[![ci](https://github.com/pawamoy/markdown-exec/workflows/ci/badge.svg)](https://github.com/pawamoy/markdown-exec/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/markdown-exec/)
[![pypi version](https://img.shields.io/pypi/v/markdown-exec.svg)](https://pypi.org/project/markdown-exec/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat)](https://gitpod.io/#https://github.com/pawamoy/markdown-exec)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/markdown-exec/community)

Utilities to execute code blocks in Markdown files.

For example, you write a Python code block that computes some HTML,
and this HTML is injected in place of the code block.

## Installation

With `pip`:
```bash
pip install markdown-exec
```

## Configuration

This extension relies on the
[SuperFences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/)
extension of
[PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/).

To allow execution of code blocks,
configure a custom fence from Python:

```python
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
                # bash, console, md, markdown, py, python, pycon, sh, tree
            ]
        }
    }
)
```

...or in MkDocs configuration file, as a Markdown extension:

```yaml
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

```yaml
# mkdocs.yml
plugins:
- search
- markdown-exec
```

## Usage

You are now able to execute code blocks instead of displaying them:

````md
```python exec="on"
print("Hello Markdown!")
```
````

The `exec` option will be true for every possible value except `0`, `no`, `off` and `false` (case insensitive).

See [usage](https://pawamoy.github.io/markdown-exec/usage/) for more details,
and the [gallery](https://pawamoy.github.io/markdown-exec/gallery/) for more examples!
