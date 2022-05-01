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

```python exec="true" show_source="tabbed-right" title="Diagrams"
from base64 import b64encode
from contextlib import suppress
from diagrams import Diagram, setdiagram
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet
from diagrams.k8s.network import Ingress, Service

with suppress(FileNotFoundError):
    with Diagram("Exposed Pod with 3 Replicas", show=False) as diagram:
        diagram.render = lambda: None
        net = Ingress("domain.com") >> Service("svc")
        net >> [Pod("pod1"),
                Pod("pod2"),
                Pod("pod3")] << ReplicaSet("rs") << Deployment("dp") << HPA("hpa")
        png = b64encode(diagram.dot.pipe(format="png")).decode()

output_html(f'<img src="data:image/png;base64, {png}"/>')
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

```python exec="true" show_source="tabbed-right" isolate="yes" title="pydeps module dependencies graph"
from pydeps import cli, colors, py2depgraph, dot
from pydeps.pydeps import depgraph_to_dotsrc
from pydeps.target import Target

cli.verbose = cli._not_verbose
options = cli.parse_args(["src/markdown_exec", "--noshow"])
colors.START_COLOR = options["start_color"]
target = Target(options["fname"])
with target.chdir_work():
    dep_graph = py2depgraph.py2dep(target, **options)
dot_src = depgraph_to_dotsrc(target, dep_graph, **options)
svg = dot.call_graphviz_dot(dot_src, "svg").decode()
svg = "".join(svg.splitlines()[6:])
svg = svg.replace('fill="white"', 'fill="transparent"')
reference = "../reference"
modules = (
    "markdown_exec",
    "markdown_exec.python",
    "markdown_exec.markdown_helpers",
)
for module in modules:
    svg_title = module.replace(".", "_")
    title_tag = f"<title>{svg_title}</title>"
    href = f"{reference}/{module.replace('.', '/')}/"
    svg = svg.replace(title_tag, f'<a href="{href}"><title>{module}</title>')
svg = svg.replace("</text></g>", "</text></a></g>")
output_html(svg)
```

## Code snippets (SVG)

[Rich](https://github.com/Textualize/rich) allows to export syntax-highlighted code as SVG.
Here we hardcode the code snippet we want to render, but we could instead include it
from somewhere else using the
[`pymdownx.snippets` extension](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/)
or by reading it dynamically from Python.
We also prevent Rich from actually writing to the terminal.

```python exec="true" show_source="tabbed-right" title="Rich SVG code snippet"
import os
from rich.console import Console
from rich.syntax import Syntax

code = """from contextlib import asynccontextmanager
import httpx


class BookClient(httpx.AsyncClient):
    async def get_book(self, book_id: int) -> str:
        response = await self.get(f"/books/{book_id}")
        return response.text


@asynccontextmanager
async def book_client(*args, **kwargs):
    async with BookClient(*args, **kwargs) as client:
        yield client
"""

with open(os.devnull, "w") as devnull:
    console = Console(record=True, width=65, file=devnull, markup=False)
    renderable = Syntax(code, "python", line_numbers=True, indent_guides=True, theme="material")
    console.print(renderable, markup=False)
svg = console.export_svg()
output_html(svg)
```

## Python module output

This example uses Python's [`runpy`][runpy] module to run another
Python module. This other module's output is captured by temporarily
patching `sys.stdout` with a text buffer. 

```python exec="true" show_source="tabbed-right" isolate="yes" title="runpy and script/module output"
import argparse
import sys
import warnings
from contextlib import suppress
from io import StringIO
from runpy import run_module

old_argv = list(sys.argv)
sys.argv = ["mkdocs"]
old_stdout = sys.stdout
sys.stdout = StringIO()
warnings.filterwarnings("ignore", category=RuntimeWarning) 
with suppress(SystemExit):
    run_module("mkdocs", run_name="__main__")
output = sys.stdout.getvalue()
sys.stdout = old_stdout
sys.argv = old_argv

output_markdown(f"```\n{output}\n```")
```

## Python CLI documentation

### Argparse help message (code block)

Instead of blindly running a module with `runpy` to get its help message,
if you know the project is using [`argparse`][argparse] to build its command line
interface, and if it exposes its parser, then you can get the help message
directly from the parser.

```python exec="true" show_source="tabbed-right" isolate="yes" title="argparse parser help message"
from duty.cli import get_parser
parser = get_parser()
output_markdown(f"```\n{parser.format_help()}\n```")
```

### Argparse parser documentation

In this example, we inspect the `argparse` parser to build better-looking
Markdown/HTML contents. We simply use the description and iterate on options,
but more complex stuff is possible of course.

```python exec="true" show_source="tabbed-right" isolate="yes" title="CLI help using argparse parser"
import argparse
from duty.cli import get_parser
parser = get_parser()
lines = []
lines.append(f"## duty")
if parser.description:
    lines.append(parser.description)
lines.append("\nOptions:\n")
for action in parser._actions:
    opts = [f"`{opt}`" for opt in action.option_strings]
    if not opts:
        continue
    line = "- " + ",".join(opts)
    if action.metavar:
        line += f" `{action.metavar}`"
    line += f": {action.help}"
    if action.default and action.default != argparse.SUPPRESS:
        line += f"(default: {action.default})"
    lines.append(line)
output_markdown("\n".join(lines))
```
