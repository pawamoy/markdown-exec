from pydeps import cli, colors, dot, py2depgraph
from pydeps.pydeps import depgraph_to_dotsrc
from pydeps.target import Target

# Note: pydeps wasn't designed to be used in such a programatic way, so the code is a bit convoluted,
# but you could make a function of it, put it in an importable script/module,
# and reuse it cleanly in your executed code blocks.

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
print(svg)
