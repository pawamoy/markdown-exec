# Usage

## HTML vs. Markdown

By default, Markdown Exec will render what you print as Markdown.
If you want to skip rendering, to inject HTML directly,
you can set the `html` option to true.

HTML Example:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
System information:

```python exec="true" html="true"
--8<-- "platform_html.py"
```
````

Markdown Example:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
System information:

```python exec="true"
--8<-- "platform_md.py"
```
````

## Render the source code as well

It's possible to render both the result of the executed code block
*and* the code block itself. For this, use the `source` option
with one of the following values:

- `above`: The source code will be rendered above the result.
- `below`: The source code will be rendered below the result.
- `material-block`: The source code and result will be wrapped in a nice-looking block (only works with Material for MkDocs).
- `tabbed-left`: The source code and result will be rendered in tabs, in that order (remember to enable the `pymdownx.tabbed` extension).
- `tabbed-right`: The result and source code will be rendered in tabs, in that order (remember to enable the `pymdownx.tabbed` extension).
- `console`: The source and result are concatenated in a single code block, like an interactive console session.

**Source above:**

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```python exec="true" source="above"
--8<-- "source.py"
```
````

---

**Source below:**

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```python exec="true" source="below"
--8<-- "source.py"
```
````

---

**Material block:**

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```python exec="true" source="material-block"
--8<-- "source.py"
```
````

---

**Tabbed on the left:**

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```python exec="true" source="tabbed-left"
--8<-- "source.py"
```
````

---

**Tabbed on the right:**

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```python exec="true" source="tabbed-right"
--8<-- "source.py"
```
````

---

**Console** <small>(best used with actual session syntax like
[`pycon`](python/#python-console-code) or [`console`](shell/#console))</small>:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```pycon exec="true" source="console"
--8<-- "source.pycon"
```
````

## Change the titles of tabs

In the previous example, we didn't specify any title for tabs,
so Markdown Exec used "Source" and "Result" by default.
You can customize the titles with the `tabs` option:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```python exec="1" source="tabbed-left" tabs="Source code|Output"
--8<-- "source.py"
```
````

As you can see, titles are separated with a pipe `|`. Both titles are stripped
so you can add space around the pipe. If you need to use that character in a title,
simply escape it with `\|`:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```python exec="1" source="tabbed-left" tabs="OR operator: a \|\|b | Boolean matrix"
--8<-- "boolean_matrix.py"
```
````

IMPORTANT: The `tabs` option ***always*** expects the "Source" tab title first,
and the "Result" tab title second. It allows to switch from tabbed-left
to tabbed-right and inversely without having to switch the titles as well.


WARNING: **Limitation**  
Changing the title for only one tab is not supported.

## Wrap result in a code block

You can wrap the result in a code block by specifying a code block language:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```console exec="1" result="json"
$ pdm info --env
```
````

WARNING: **Limitation**  
Wrapping the result is not possible when HTML output is enabled,
nor when source and output are concatenated with the "console" style.

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

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```python exec="1" source="above" title="source.py"
--8<-- "source.py"
```
````

## Literate Markdown

With this extension, it is also possible to write "literate programming" Markdown.

From [Wikipedia](https://en.wikipedia.org/wiki/Literate_programming):

> Literate programming (LP) tools are used to obtain two representations from a source file:
  one understandable by a compiler or interpreter, the "tangled" code,
  and another for viewing as formatted documentation, which is said to be "woven" from the literate source.

We effectively support executing multiple *nested* code blocks to generate complex output.
That makes for a very meta-markdown markup:

````md exec="1" source="tabbed-left"
```md exec="1" source="material-block" title="Markdown link"
[Link to example.com](https://example.com)
```
````

> TIP: **So power, such meta**  
> The above example (both tabs) was entirely generated using *a literate code block in a literate code block* 🤯:
> 
> `````md
> ````md exec="1" source="tabbed-left"
> ```md exec="1" source="material-block" title="Markdown link"
> [Link to example.com](https://example.com)
> ```
> ````
> `````
>
> In fact, all the examples on this page were generated using this method!
> Check out the source here: https://github.com/pawamoy/markdown-exec/blob/master/docs/usage.md
> (click on "Raw" to see the code blocks execution options).

Of course "executing" Markdown (or rather, making it "literate") only makes sense when the source is shown as well.
