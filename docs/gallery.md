---
hide:
- navigation
---

# Gallery

Welcome to our gallery of examples!

## Diagrams, charts, graphs, plots

### with [Diagrams](https://github.com/mingrammer/diagrams)

> Diagram as Code for prototyping cloud system architectures.

````md exec="1" source="tabbed-right"
```python exec="true" html="true"
--8<-- "gallery/diagrams.py"
```
````

### with [D2](https://d2lang.com/)

> A modern diagram scripting language that turns text to diagrams. 

````md exec="1" source="tabbed-right"
```python exec="true" html="true"
--8<-- "gallery/d2.py"
```
````

### with [Matplotlib](https://matplotlib.org/)

> Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.

````md exec="1" source="tabbed-right"
```python exec="1" html="1"
--8<-- "gallery/matplotlib.py"
```
````

### with [pipdeptree](https://github.com/tox-dev/pipdeptree)

> A command line utility to display dependency tree of the installed Python packages.

We call `pipdeptree` with its `--mermaid` option to generate a [Mermaid](https://mermaid.js.org/) diagram.

````md exec="1" source="tabbed-right"
```bash exec="1" result="mermaid"
# Change the direction of the graph from top-down to left-right,
# and remove local version identifiers from our own package.
pipdeptree -p markdown-exec --mermaid 2>/dev/null |
    sed -E 's/\.dev.+"\]$/"]/;s/\+d.*"\]$/"]/'
```
````

Another example with more dependencies:

````md exec="1" source="tabbed-right"
```bash exec="1" result="mermaid"
pipdeptree -p mkdocstrings-python --mermaid 2>/dev/null |
    sed 's/flowchart TD/flowchart LR/'
```
````

### with [Plotly](https://plotly.com/python/)

> The interactive graphing library for Python ✨

````md exec="1" source="tabbed-right"
```python exec="true" html="true"
--8<-- "gallery/plotly.py"
```
````

### with [pydeps](https://github.com/thebjorn/pydeps)

> Python Module Dependency graphs.

pydeps uses [Graphviz](https://graphviz.org/) under the hood to generate graphs. In this example we add links to the code reference in related nodes. Try clicking on the `markdown_exec` nodes!

````md exec="1" source="tabbed-right"
```python exec="true" html="true"
--8<-- "gallery/pydeps.py"
```
````

## Code snippets

### with [Rich](https://github.com/Textualize/rich)

> Rich is a Python library for rich text and beautiful formatting in the terminal.

````md exec="1" source="tabbed-right"
```python exec="true" html="true"
--8<-- "gallery/rich.py"
```
````

### with [PyTermGUI](https://github.com/bczsalba/pytermgui)

> Python TUI framework with mouse support, modular widget system, customizable and rapid terminal markup language and more!

````md exec="1" source="tabbed-right"
```python exec="true" html="true"
--8<-- "gallery/pytermgui.py"
```
````

TIP: There's a PyTermGUI-dedicated MkDocs plugin that allows to generate SVGs on-the-fly: [Termage](https://github.com/bczsalba/Termage). It is implemented using regular expressions in the `on_markdown` event of MkDocs, so is probably less robust than our actual SuperFence implementation here, but also allows for less verbose source to generate the SVG snippets.

## Console output

If you installed Markdown Exec with the `ansi` extra (`pip install markdown-exec[ansi]`), the ANSI colors in the output of shell commands will be translated to HTML/CSS, allowing to render them naturally in your documentation pages. For this to happen, use the [`result="ansi"` option](http://localhost:8000/markdown-exec/usage/#wrap-result-in-a-code-block).

````md exec="1" source="tabbed-right"
```bash exec="true" result="ansi"
--8<-- "gallery/ansi.sh"
```
````

### with [Rich](https://github.com/Textualize/rich)

> Rich is a Python library for rich text and beautiful formatting in the terminal.

````md exec="1" source="tabbed-right"
```python exec="true" html="true"
--8<-- "gallery/rich_terminal.py"
```
````

## SVG drawings

### with [Chalk](https://github.com/chalk-diagrams/chalk)

> A declarative drawing API in Python.

````md exec="1" source="tabbed-right"
```python exec="true" html="true"
--8<-- "gallery/chalk.py"
```
````
### with [Drawsvg 2](https://github.com/cduck/drawsvg)

> Programmatically generate SVG (vector) images, animations, and interactive Jupyter widgets.

````md exec="1" source="tabbed-right"
```python exec="true" html="true"
--8<-- "gallery/drawsvg.py"
```
````

### with [Hyperbolic](https://github.com/cduck/hyperbolic)

> A Python 3 library for constructing and drawing hyperbolic geometry.

````md exec="1" source="tabbed-right"
```python exec="true" html="true"
--8<-- "gallery/hyperbolic.py"
```
````

## QRCodes

### with [qrcode](https://pypi.org/project/qrcode/)

> Python QR Code image generator.

````md exec="1" source="tabbed-right"
```python exec="true" html="true"
--8<-- "gallery/qrcode.py"
```
````

## TUI screenshots

### with [Textual](https://github.com/Textualize/textual)

> Textual is a *Rapid Application Development* framework for Python, built by [Textualize.io](https://www.textualize.io/).

````md exec="1" source="tabbed-right"
```python exec="1" html="true"
--8<-- "gallery/textual.py"
```
````

## Python CLI documentation

### with [`argparse`](https://docs.python.org/3/library/argparse.html#module-argparse) (code block)

If you know a project is using `argparse` to build its command line interface, and if it exposes its parser, then you can get the help message directly from the parser.

````md exec="1" source="tabbed-right"
```python exec="true"
--8<-- "gallery/argparse_format.py"
```
````

### with [`argparse`](https://docs.python.org/3/library/argparse.html#module-argparse) (Markdown)

In this example, we inspect the `argparse` parser to build better-looking Markdown/HTML contents. We simply use the description and iterate on options, but more complex stuff is possible of course.

````md exec="1" source="tabbed-right"
```python exec="true" updatetoc="no"
--8<-- "gallery/argparse.py"
```
````

## Other techniques

### with [`runpy`](https://docs.python.org/3/library/runpy.html#module-runpy)

This example uses Python's `runpy` module to run another Python module. This other module's output is captured by temporarily patching `sys.stdout` with a text buffer.

````md exec="1" source="tabbed-right"
```python exec="true"
--8<-- "gallery/runpy.py"
```
````
