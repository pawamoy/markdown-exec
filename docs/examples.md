## Draw a graph of module inter-dependencies with [pydeps](https://github.com/thebjorn/pydeps)

````md
```python exec="true"
````
```python
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
svg = svg.replace('fill="white"', 'fill="transparent"')
output_html(f"<div>{svg}</div>")
```
````
```
````
