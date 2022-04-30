## Draw a graph of module inter-dependencies with [pydeps](https://github.com/thebjorn/pydeps)

```python exec="true" show_source="tabbed-right" isolate="yes"
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
modules_map = {
    "markdown_exec": "../reference/markdown_exec/",
    "markdown_exec_python": "../reference/markdown_exec/python/",
    "markdown_exec_utils": "../reference/markdown_exec/utils/",
}
for title, href in modules_map.items():
    title_tag = f"<title>{title}</title>"
    svg = svg.replace(title_tag, f'<a href="{href}">' + title_tag)
svg = svg.replace("</text></g>", "</text></a></g>")
output_html(svg)
```

## Run a Python module and print its output

```python exec="true" show_source="tabbed-right" isolate="yes"
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

## Format help of a CLI tool based on argparse in a code block

```python exec="true" show_source="tabbed-right" isolate="yes"
from duty.cli import get_parser
parser = get_parser()
output_markdown(f"```\n{parser.format_help()}\n```")
```

## Format help of a CLI tool based on argparse as Markdown

```python exec="true" show_source="tabbed-right" isolate="yes"
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

## Draw a diagram using the [Diagrams](https://github.com/mingrammer/diagrams) library

```python exec="true" show_source="tabbed-right"
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

## Build an SVG image from code snippets with [Rich](https://github.com/Textualize/rich)

```python exec="true" show_source="tabbed-right"
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