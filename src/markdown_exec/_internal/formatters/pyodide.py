# Formatter for creating a Pyodide interactive editor.

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from markdown import Markdown

# All Ace.js themes listed here:
# https://github.com/ajaxorg/ace/tree/master/src/theme

_play_emoji = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M8 5.14v14l11-7-11-7Z"></path></svg>'
)
_clear_emoji = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15.14 3c-.51 0-1.02.2-1.41.59L2.59 14.73c-.78.77-.78 2.04 0 2.83L5.03 20h7.66l8.72-8.73c.79-.77.79-2.04 0-2.83l-4.85-4.85c-.39-.39-.91-.59-1.42-.59M17 18l-2 2h7v-2"></path></svg>'

_assets = """
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.16.0/ace.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/pyodide/v{version}/full/pyodide.js"></script>
<link title="light" rel="alternate stylesheet" href="https://cdn.jsdelivr.net/npm/highlightjs-themes@1.0.0/tomorrow.min.css" disabled="disabled">
<link title="dark" rel="alternate stylesheet" href="https://cdn.jsdelivr.net/npm/highlightjs-themes@1.0.0/tomorrow-night-blue.min.css" disabled="disabled">
"""

_template = """
<div class="pyodide">
<div class="pyodide-editor-bar">
<span class="pyodide-bar-item">Editor (session: %(session)s)</span><span id="%(id_prefix)srun" title="Run: press Ctrl-Enter" class="pyodide-bar-item pyodide-clickable"><span class="twemoji">%(play_emoji)s</span> Run</span>
</div>
<div><pre id="%(id_prefix)seditor" class="pyodide-editor" style="height: %(height)spx; min-height: %(min_height)spx; max-height: %(max_height)spx; resize: %(resize)s;">%(initial_code)s</pre></div>
<div class="pyodide-editor-bar">
<span class="pyodide-bar-item">Output</span><span id="%(id_prefix)sclear" class="pyodide-bar-item pyodide-clickable"><span class="twemoji">%(clear_emoji)s</span> Clear</span>
</div>
<pre><code id="%(id_prefix)soutput" class="pyodide-output"></code></pre>
</div>

<script>
document.addEventListener('DOMContentLoaded', (event) => {
    setupPyodide('%(id_prefix)s', install=%(install)s, themeLight='%(theme_light)s', themeDark='%(theme_dark)s', session='%(session)s');
});
</script>
"""

_counter = 0


def _format_pyodide(code: str, md: Markdown, session: str, extra: dict, **options: Any) -> str:  # noqa: ARG001
    global _counter  # noqa: PLW0603
    _counter += 1
    version = extra.pop("version", "0.26.4").lstrip("v")
    install = extra.pop("install", "")
    install = install.split(",") if install else []
    exclude_assets = extra.pop("assets", "1").lower() in {"0", "false", "no", "off"}
    theme = extra.pop("theme", "tomorrow,tomorrow_night")
    if "," not in theme:
        theme = f"{theme},{theme}"
    theme_light, theme_dark = theme.split(",")
    
    # Get height configuration parameters with defaults
    # Get the number of lines from extra parameters, default to 10 lines
    lines = int(extra.pop("lines", "10"))
    # Calculate editor height based on line count with a more accurate line height
    # Adding a small buffer to account for editor chrome
    line_height = 22  # Increase from 20px to 22px per line
    padding = 10      # Add some padding to account for editor UI elements
    editor_height = (lines * line_height) + padding
    
    # Calculate default height based on line count
    default_height = lines * line_height
    
    # Get explicit height configurations if provided
    height = extra.pop("height", str(default_height))
    min_height = extra.pop("min_height", str(default_height))
    max_height = extra.pop("max_height", "400")
    
    # Get resize option (none, both, vertical, horizontal)
    resize = extra.pop("resize", "none")
    
    # Convert to integers if they're numeric
    try:
        height = int(height)
    except ValueError:
        pass
    
    try:
        min_height = int(min_height)
    except ValueError:
        pass
    
    try:
        max_height = int(max_height)
    except ValueError:
        pass

    data = {
        "id_prefix": f"exec-{_counter}--",
        "initial_code": code,
        "install": install,
        "theme_light": theme_light.strip(),
        "theme_dark": theme_dark.strip(),
        "session": session or "default",
        "play_emoji": _play_emoji,
        "clear_emoji": _clear_emoji,
        "height": height,
        "min_height": min_height,
        "max_height": max_height,
        "resize": resize,
    }
    rendered = _template % data
    if exclude_assets:
        return rendered
    return _assets.format(version=version) + rendered
