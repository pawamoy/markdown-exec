# Markdown Exec

[![ci](https://github.com/pawamoy/markdown-exec/workflows/ci/badge.svg)](https://github.com/pawamoy/markdown-exec/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/markdown-exec/)
[![pypi version](https://img.shields.io/pypi/v/markdown-exec.svg)](https://pypi.org/project/markdown-exec/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat)](https://gitpod.io/#https://github.com/pawamoy/markdown-exec)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/markdown-exec/community)

Utilities to execute code blocks in Markdown files.

For example, you write a Python code block that computes some HTML,
and this HTML is injected in place of the code block.

## Requirements

Markdown Exec requires Python 3.7 or above.

<details>
<summary>To install Python 3.7, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.7
pyenv install 3.7.12

# make it available globally
pyenv global system 3.7.12
```
</details>

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
            ]
        }
    }
)
```

...or in MkDocs configuration file:

```yaml
markdown_extensions:
- pymdownx.superfences:
    custom_fences:
    - name: python
      class: python
      validator: !!python/name:markdown_exec.validator
      format: !!python/name:markdown_exec.formatter
```

## Usage

You are now able to execute code blocks instead of displaying them:

````md
```python exec="on"
print("Some Python code")
```
````

The `exec` option will be true for every possible value except `0`, `no`, `off` and `false` (case insensitive).

The standard output and error of executed Python code blocks is not captured
and will be written to the terminal, as usual.

If you want to "inject" contents into the page, you can use these two functions
in your code blocks (they are available in the global context of execution):

- `output_html(text)`: inject the HTML text passed as argument. 
- `output_markdown(text)`: convert the text passed as argument to HTML and then inject it.

WARNING: You can call these functions only once, as they internally raise an exception.

HTML Example:

=== "Markdown"

    ````md
    System information:

    ```python exec="yes"
    import platform
    output_html(
        f"""
        <code>
        machine: {platform.machine()}
        version: {platform.version()}
        platform: {platform.platform()}
        system: {platform.system()}
        </code>
        """
    )
    ```
    ````

=== "Rendered"

    System information:

    ```
    machine: x86_64
    version: #1 SMP PREEMPT Tue, 01 Feb 2022 21:42:50 +0000
    platform: Linux-5.16.5-arch1-1-x86_64-with-glibc2.33
    system: Linux
    ```

Markdown Example:

=== "Markdown"

    ````md
    System information:

    ```python exec="yes"
    import platform
    output_markdown(
        f"""
        - machine: `{platform.machine()}`
        - version: `{platform.version()}`
        - platform: `{platform.platform()}`
        - system: `{platform.system()}`
        """
    )
    ```
    ````

=== "Rendered"

    System information:

    - machine: `x86_64`
    - version: `#1 SMP PREEMPT Tue, 01 Feb 2022 21:42:50 +0000`
    - platform: `Linux-5.16.5-arch1-1-x86_64-with-glibc2.33`
    - system: `Linux`