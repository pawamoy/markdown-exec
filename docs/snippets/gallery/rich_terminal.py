import os

from rich.console import Console

report = """$ griffe check griffe -ssrc -b0.24.0 -a0.23.0
[bold]src/griffe/loader.py[/]:156: GriffeLoader.resolve_aliases([#7faeff]only_exported[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
[bold]src/griffe/loader.py[/]:156: GriffeLoader.resolve_aliases([#7faeff]only_exported[/]): [#afaf72]Parameter default was changed[/]: True -> None
[bold]src/griffe/loader.py[/]:156: GriffeLoader.resolve_aliases([#7faeff]only_known_modules[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
[bold]src/griffe/loader.py[/]:156: GriffeLoader.resolve_aliases([#7faeff]only_known_modules[/]): [#afaf72]Parameter default was changed[/]: True -> None
[bold]src/griffe/loader.py[/]:156: GriffeLoader.resolve_aliases([#7faeff]max_iterations[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
[bold]src/griffe/loader.py[/]:308: GriffeLoader.resolve_module_aliases([#7faeff]only_exported[/]): [#afaf72]Parameter was removed[/]
[bold]src/griffe/loader.py[/]:308: GriffeLoader.resolve_module_aliases([#7faeff]only_known_modules[/]): [#afaf72]Parameter was removed[/]
[bold]src/griffe/git.py[/]:39: tmp_worktree([#7faeff]commit[/]): [#afaf72]Parameter was removed[/]
[bold]src/griffe/git.py[/]:39: tmp_worktree([#7faeff]repo[/]): [#afaf72]Positional parameter was moved[/]: position: from 2 to 1 (-1)
[bold]src/griffe/git.py[/]:75: load_git([#7faeff]commit[/]): [#afaf72]Parameter was removed[/]
[bold]src/griffe/git.py[/]:75: load_git([#7faeff]repo[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
[bold]src/griffe/git.py[/]:75: load_git([#7faeff]submodules[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
[bold]src/griffe/git.py[/]:75: load_git([#7faeff]try_relative_path[/]): [#afaf72]Parameter was removed[/]
[bold]src/griffe/git.py[/]:75: load_git([#7faeff]extensions[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
[bold]src/griffe/git.py[/]:75: load_git([#7faeff]search_paths[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
[bold]src/griffe/git.py[/]:75: load_git([#7faeff]docstring_parser[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
[bold]src/griffe/git.py[/]:75: load_git([#7faeff]docstring_options[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
[bold]src/griffe/git.py[/]:75: load_git([#7faeff]lines_collection[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
[bold]src/griffe/git.py[/]:75: load_git([#7faeff]modules_collection[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
[bold]src/griffe/git.py[/]:75: load_git([#7faeff]allow_inspection[/]): [#afaf72]Parameter kind was changed[/]: positional or keyword -> keyword-only
"""

with open(os.devnull, "w") as devnull:
    console = Console(record=True, width=150, file=devnull)
    console.print(report, markup=True, highlight=False)
print(console.export_html(inline_styles=True, code_format="<pre><code>{code}</code></pre>"))
