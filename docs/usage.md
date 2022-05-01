## HTML vs. Markdown

By default, Markdown Exec will render what you print as Markdown.
If you want to skip rendering, to inject HTML directly,
you can set the `html` option to true.

HTML Example:

=== "Markdown"

    ````md
    System information:

    ```python exec="true" html="true"
    --8<-- "platform_html.py"
    ```
    ````

=== "Rendered"

    System information:

    ```python exec="1" html="1"
    --8<-- "platform_html.py"
    ```

Markdown Example:

=== "Markdown"

    ````md
    System information:

    ```python exec="true"
    --8<-- "platform_md.py"
    ```
    ````

=== "Rendered"

    System information:

    ```python exec="1"
    --8<-- "platform_md.py"
    ```

## Render the source code as well

It's possible to render both the result of the executed code block
*and* the code block itself. For this, use the `source` option
with one of the following values:

- `above`: The source code will be rendered above the result.
- `below`: The source code will be rendered below the result.
- `tabbed-left`: The source code and result will be rendered in tabs, in that order (remember to enable the `pymdownx.tabbed` extension).
- `tabbed-right`: The result and source code will be rendered in tabs, in that order (remember to enable the `pymdownx.tabbed` extension).

Source above:

=== "Markdown"

    ````md
    ```python exec="true" source="above"
    --8<-- "source.py"
    ```
    ````

=== "Rendered"

    ```python exec="true" source="above"
    --8<-- "source.py"
    ```

Source below:

=== "Markdown"

    ````md
    ```python exec="true" source="below"
    --8<-- "source.py"
    ```
    ````

=== "Rendered"

    ```python exec="true" source="below"
    --8<-- "source.py"
    ```

Tabbed on the left:

=== "Markdown"

    ````md
    ```python exec="true" source="tabbed-left"
    --8<-- "source.py"
    ```
    ````

=== "Rendered"

    ```python exec="true" source="tabbed-left"
    --8<-- "source.py"
    ```

Tabbed on the right:

=== "Markdown"

    ````md
    ```python exec="true" source="tabbed-right"
    --8<-- "source.py"
    ```
    ````

=== "Rendered"

    ```python exec="true" source="tabbed-right"
    --8<-- "source.py"
    ```

## Change the titles of tabs

In the previous example, we didn't specify any title for tabs,
so Markdown Exec used "Source" and "Result" by default.
You can customize the titles with the `tabs` option:

=== "Markdown"

    ````md
    ```python exec="1" source="tabbed-left" tabs="Source code|Output"
    --8<-- "source.py"
    ```
    ````

=== "Rendered"

    ```python exec="1" source="tabbed-left" tabs="Source code|Output"
    --8<-- "source.py"
    ```

As you can see, titles are separated with a pipe `|`. Both titles are stripped
so you can add space around the pipe. If you need to use that character in a title,
simply escape it with `\|`:

=== "Markdown"

    ````md
    ```python exec="1" source="tabbed-left" tabs="OR operator: a \|\|b | Boolean matrix"
    --8<-- "boolean_matrix.py"
    ```
    ````

=== "Rendered"

    ```python exec="1" source="tabbed-left" tabs="OR operator: a \|\| b | Boolean matrix"
    --8<-- "boolean_matrix.py"
    ```

IMPORTANT: The `tabs` option ***always*** expects the "Source" tab title first,
and the "Result" tab title second. It allows to switch from tabbed-left
to tabbed-right and inversely without having to switch the titles as well.


WARNING: **Limitation**  
Changing the title for only one tab is not supported.

## Additional options

If you are using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/),
you are probably familiar with the `title` option on code blocks:

````md
```python title="setup.py"
from setuptools import setup
setup(...)
```
````

Markdown Exec will add back these unrecognized options
when rendering the source, so you can keep using them normally.

Example:

=== "Markdown"

    ````md
    ```python exec="1" source="above" title="source.py"
    --8<-- "source.py"
    ```
    ````

=== "Rendered"

    ```python exec="1" source="above" title="source.py"
    --8<-- "source.py"
    ```