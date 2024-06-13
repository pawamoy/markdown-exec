# Pyodide

[:octicons-tag-24: Insiders 1.0.0](../insiders/changelog.md#1.0.0)

This special `pyodide` fence uses [Pyodide](https://pyodide.org), [Ace](https://ace.c9.io/)
and [Highlight.js](https://highlightjs.org/) to render an interactive Python editor.
Everything runs on the client side. The first time Pyodide is loaded by the browser
can be a bit long, but then it will be cached and the next time you load the page
it will be much faster.

Click the **:material-play: Run** button in the top-right corner, or hit ++ctrl+enter++ to run the code.
You can install packages with Micropip:

````md exec="1" source="tabbed-right" tabs="Markdown|Rendered"
```pyodide
import micropip

print("Installing cowsay...")
await micropip.install("cowsay")
print("done!")
```
````

Then you can import and use the packages you installed:

````md exec="1" source="tabbed-right" tabs="Markdown|Rendered"
```pyodide
import cowsay
cowsay.cow("Hello World")
```
````

Packages installed with Micropip are cached by the browser as well,
making future installations much faster.

## Sessions

Editors with the same session share the same `globals()` dictionary,
so you can reuse variables, classes, imports, etc., from another editor
within the same session. This is why you can import `cowsay` in this editor,
given you actually installed it in the first. Sessions are ephemeral:
everything is reset when reloading the page. This means you cannot persist
sessions across multiple pages. Try refreshing your page
and running the code of the second editor: you should get a ModuleNotFoundError.

To use other sessions, simply pass the `session="name"` option to the code block:

````md exec="1" source="tabbed-right" tabs="Markdown|Rendered"
```pyodide session="something"
something = "hello"
```
````

Now lets print it in another editor with the same session:

````md exec="1" source="tabbed-right" tabs="Markdown|Rendered"
```pyodide session="something"
print(something)
```
````

And in another editor with the default session:

````md exec="1" source="tabbed-right" tabs="Markdown|Rendered"
```pyodide
print(something)
```
````

## Pre-installing packages

In your own documentation pages, you might not want to add
`import micropip; await micropip.install("your-package")`
to every editor to show how to use your package. In this case,
you can use the `install` option to pre-install packages.
The option takes a list of comma-separated package distribution names:

````md exec="1" source="tabbed-right" tabs="Markdown|Rendered"
```pyodide install="griffe,dependenpy"
import griffe
import dependenpy
print("OK!")
```
````

## Excluding assets

When you add a Pyodide fence to a page,
Markdown Exec will inject `<script>` and `<link>` tags
to load Javascript and CSS assets.
If you add multiple Pyodide fences to the same page,
the same assets will be included many times.
The browser is clever enough not to re-download them everytime
(they are cached), but we can still avoid re-injecting assets
to make the HTML page smaller and faster.

````md
```pyodide assets="no"
print("hello")
```
````

**Make sure that at least one Pyodide fence per page injects the assets.**

## Editor themes

The editor provided by [Ace](https://ace.c9.io/) supports different color themes.
The complete list can be found here: https://github.com/ajaxorg/ace/tree/master/src/theme.

To use a specific theme for both light and dark schemes, use the `theme` option on the Pyodide code block:

````md
```pyodide theme="ambiance"
print("hello")
```
````

To specify different themes for the light and dark schemes, separate them with a comma:

````md
```pyodide theme="ambiance,chaos"
print("hello")
```
````

See all previews below.

```python exec="1"
import subprocess
from textwrap import dedent

theme_files = subprocess.check_output(["gh", "api", "/repos/ajaxorg/ace/contents/src/theme", "--jq", ".[].name"], text=True)
themes = [theme_file[:-3] for theme_file in theme_files.splitlines() if not theme_file.endswith("-css.js")]
for theme in themes:
    print(f"### `{theme}`")
    print(
        dedent(
            f'''
            ```pyodide theme="{theme}" assets="no"
            from typing import Iterator

            # This is an example
            class Math:
                @staticmethod
                def fib(n: int) -> Iterator[int]:
                    """Fibonacci series up to n."""
                    a, b = 0, 1
                    while a < n:
                        yield a
                        a, b = b, a + b

            result = sum(Math.fib(42))
            print(f"The answer is {{result}}")
            ```
            '''
        )
    )
```
