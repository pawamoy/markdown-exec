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