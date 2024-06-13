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
reference = "../reference"
modules = (
    "markdown_exec",
    "markdown_exec.formatters",
    "markdown_exec.formatters.base",
    "markdown_exec.formatters.bash",
    "markdown_exec.formatters.console",
    "markdown_exec.formatters.markdown",
    "markdown_exec.formatters.pycon",
    "markdown_exec.formatters.pyodide",
    "markdown_exec.formatters.python",
    "markdown_exec.formatters.sh",
    "markdown_exec.formatters.tree",
    "markdown_exec.logger",
    "markdown_exec.mkdocs_plugin",
    "markdown_exec.processors",
    "markdown_exec.rendering",
)
for module in modules:
    svg_title = module.replace(".", "_")
    title_tag = f"<title>{svg_title}</title>"
    href = f"{reference}/{module.replace('.', '/')}/"
    svg = svg.replace(title_tag, f'<a href="{href}"><title>{module}</title>')
svg = svg.replace("</text></g>", "</text></a></g>")
print(svg)
