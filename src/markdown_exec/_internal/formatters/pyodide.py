# Formatter for creating a Pyodide interactive editor.

from __future__ import annotations

import json
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
<div><pre id="%(id_prefix)seditor" class="pyodide-editor">%(initial_code)s</pre></div>
<div class="pyodide-editor-bar">
<span class="pyodide-bar-item">Output</span><span id="%(id_prefix)sclear" class="pyodide-bar-item pyodide-clickable"><span class="twemoji">%(clear_emoji)s</span> Clear</span>
</div>
<pre><code id="%(id_prefix)soutput" class="pyodide-output"></code></pre>
</div>

<script>
document.addEventListener('DOMContentLoaded', (event) => {
    setupPyodide('%(id_prefix)s', install=%(install)s, themeLight='%(theme_light)s', themeDark='%(theme_dark)s', session='%(session)s', heightConfig=%(height_config)s);
});
</script>
"""

_counter = 0


def _calculate_height_config(code: str, extra: dict) -> dict:
    """Calculate height configuration for the Pyodide editor."""
    # Get per-block options with defaults
    height = extra.pop("height", "auto")
    min_height = extra.pop("min_height", 5)
    max_height = extra.pop("max_height", 30)
    resize = extra.pop("resize", True)

    # Validate and convert types
    if isinstance(height, str) and height != "auto":
        try:
            height = int(height)
        except ValueError:
            height = "auto"

    if height != "auto" and isinstance(height, int) and height <= 0:
        height = "auto"

    try:
        min_height = max(1, int(min_height))
        max_height = max(min_height, int(max_height))
    except ValueError:
        min_height, max_height = 5, 30

    try:
        resize = str(resize).lower() in ("true", "1", "yes", "on")
    except (ValueError, AttributeError):
        resize = True

    # Calculate actual height if "auto"
    if height == "auto":
        # Count lines in the code, with a reasonable default
        lines = len(code.strip().split("\n")) if code.strip() else 5
        height = max(min_height, min(lines, max_height))

    return {
        "height": height,
        "minLines": min_height,
        "maxLines": max_height,
        "resize": resize,
    }


def _format_pyodide(code: str, md: Markdown, session: str, extra: dict, **options: Any) -> str:  # noqa: ARG001
    global _counter  # noqa: PLW0603
    _counter += 1

    # Calculate height configuration for this specific code block
    height_config = _calculate_height_config(code, extra)

    version = extra.pop("version", "0.26.4").lstrip("v")
    install = extra.pop("install", "")
    install = install.split(",") if install else []
    exclude_assets = extra.pop("assets", "1").lower() in {"0", "false", "no", "off"}
    theme = extra.pop("theme", "tomorrow,tomorrow_night")
    if "," not in theme:
        theme = f"{theme},{theme}"
    theme_light, theme_dark = theme.split(",")

    # Convert height_config to JSON string for JavaScript
    height_config_json = json.dumps(height_config)

    data = {
        "id_prefix": f"exec-{_counter}--",
        "initial_code": code,
        "install": install,
        "theme_light": theme_light.strip(),
        "theme_dark": theme_dark.strip(),
        "session": session or "default",
        "play_emoji": _play_emoji,
        "clear_emoji": _clear_emoji,
        "height_config": height_config_json,
    }
    rendered = _template % data
    if exclude_assets:
        return rendered
    return _assets.format(version=version) + rendered
