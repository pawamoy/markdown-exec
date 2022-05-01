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

