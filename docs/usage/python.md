# Python

## Regular Python

Python code is executed in the current process,
with isolated global variables.

To capture the output of your code, Markdown Exec patches the `print`
function so that it writes to a buffer instead of standard output.

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```python exec="1"
print("**Hello world!**")
```
````

See the [Gallery](../gallery.md) for more complex examples.

## Python console code

Code blocks syntax-highlighted with the `pycon` identifier are also supported.
These code blocks will be pre-processed to keep only the lines
starting with `>>> `, and the chevrons (prompt) will be removed from these lines,
so we can execute them.

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```pycon exec="1" source="console"
--8<-- "usage/source.pycon"
```
````

It also means that multiple blocks of instructions will be concatenated,
as well as their output:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```pycon exec="1" source="console"
--8<-- "usage/multiple.pycon"
```
````

### Interactive console

When the `interactive` flag is set, `pycon` blocks will use an alternative formatter that mimics the behavior of the Python REPL interpreter.

In this mode outputs are displayed immediately after their source lines, rather than all outputs being shown at the end.
Additionally, outputs from unbound expressions are displayed automatically (although `print` can still be used as well).

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```pycon exec="1" interactive="1"
--8<-- "usage/interactive.pycon"
```
````

Exceptions are also handled differently: when a line raises an exception other lines in the same block are still executed and displayed as normal.
The raised exception is printed after the generating line and logged as a warning

=== "Source"
    ````md
    ```pycon exec="1" interactive="1" id="pycon_error"
    >>> y = 2
    >>> y / 0
    >>> y * 2
    ```
    ````
=== "Rendered"
    ```pycon
    >>> y = 2
    >>> y / 0
    Traceback (most recent call last):
    File "<code block: id pycon_error>", line 3, in <module>
        >>> y / 0
            ~~^~~
    ZeroDivisionError: division by zero
    >>> y * 2
    4
    ```
=== "MkDocs output"
    ```text
    WARNING  -  markdown_exec: Unexpected exception while executing pycon code block 'pycon_error':

    Traceback (most recent call last):
        File "<code block: id pycon_error>", line 3, in <module>
        >>> y / 0
            ~~^~~
    ZeroDivisionError: division by zero
    ```
