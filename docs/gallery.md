---
hide:
- navigation
---

# Gallery

Welcome to our gallery of examples!

## Diagrams (cloud/system architecture)

[Diagrams](https://github.com/mingrammer/diagrams) offers a nice way of building
diagrams. It also bundles a number of images used to illustrate objects and concepts
so you can build good-looking diagrams. By default, Diagrams tries to write
the result on disk, so we prevent that by patching its `render` method,
and by ignoring the `FileNotFoundError` that ensues. Then we use its internal
`dot` object and its `pipe` method to store the diagram in a variable,
as base64 encoded PNG data. Finally we output an HTML image with the base64 data.
Using SVG is not possible here since Diagrams embeds actual, smaller PNG files
in the result, files which are not automatically added to the final site.

```python exec="true" html="true" source="tabbed-right" title="Diagrams"
--8<-- "gallery/diagrams.py"
```

## Python modules inter-dependencies

This example uses [pydeps](https://github.com/thebjorn/pydeps) to build a graph
of interdependencies of your project's modules. Data is built and stored
in a pydeps data structure, then translated to `dot` source, then rendered to SVG
with [Graphviz](https://graphviz.org/). In this example we also add links
to the code reference in related nodes. Try clicking on the `markdown_exec` nodes!

NOTE: pydeps wasn't designed to be used in such a programatic way,
so the code is a bit convoluted, but you could make a function of it,
put it in an importable script/module, and reuse it cleanly in your executed
code blocks.

```python exec="true" html="true" source="tabbed-right" title="pydeps module dependencies graph"
--8<-- "gallery/pydeps.py"
```

## Code snippets

[Rich](https://github.com/Textualize/rich) allows to export syntax-highlighted code as SVG.
Here we hardcode the code snippet we want to render, but we could instead include it
from somewhere else using the
[`pymdownx.snippets` extension](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/)
or by reading it dynamically from Python.
We also prevent Rich from actually writing to the terminal.

```python exec="true" html="true" source="tabbed-right" title="Rich SVG code snippet"
--8<-- "gallery/rich.py"
```

<!--

Similarly, [PyTermGUI](https://github.com/bczsalba/pytermgui) also allows
to export syntax-highlighted code as SVG.

python exec="true" html="true" source="tabbed-right" title="PyTermGUI SVG code snippet"
--8<-- "gallery/pytermgui.py"

TIP: There's a PyTermGUI-dedicated MkDocs plugin that allows
to generate SVGs on-the-fly: [Termage](https://github.com/bczsalba/Termage).
It is implemented using regular expressions in the `on_markdown` event of MkDocs,
so is probably less robust than our actual SuperFence implementation here,
but also allows for less verbose source to generate the SVG snippets.

-->

## TUI screenshots

[Textual](https://github.com/Textualize/textual) allows to build Terminal User Interfaces (TUIs).
In this example we generate the SVG image of a terminal interface.

WARNING: **Not released yet.**  
The code in this example is using the CSS branch of Textual, which is not yet merged/released.

```python exec="1" html="true" source="tabbed-right" tabs="Source|Result"
--8<-- "gallery/textual.py"
```

## Charts and Plots

With [Matplotlib](https://matplotlib.org/):

```python exec="1" html="1" source="tabbed-right" title="matplotlib graph"
--8<-- "gallery/matplotlib.py"
```

## Python module output

This example uses Python's [`runpy`][runpy] module to run another
Python module. This other module's output is captured by temporarily
patching `sys.stdout` with a text buffer. 

```python exec="true" source="tabbed-right" title="runpy and script/module output"
--8<-- "gallery/runpy.py"
```

## Python CLI documentation

### Argparse help message (code block)

Instead of blindly running a module with `runpy` to get its help message,
if you know the project is using [`argparse`][argparse] to build its command line
interface, and if it exposes its parser, then you can get the help message
directly from the parser.

```python exec="true" source="tabbed-right" title="argparse parser help message"
--8<-- "gallery/argparse_format.py"
```

### Argparse parser documentation

In this example, we inspect the `argparse` parser to build better-looking
Markdown/HTML contents. We simply use the description and iterate on options,
but more complex stuff is possible of course.

```python exec="true" source="tabbed-right" title="CLI help using argparse parser"
--8<-- "gallery/argparse.py"
```
