# Formatter for file-system trees.

from __future__ import annotations

import re
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from markupsafe import Markup

from markdown_exec._internal.rendering import MarkdownConverter, code_block

try:
    import material
except ImportError:
    material = None

if TYPE_CHECKING:
    from markdown import Markdown


if material is not None:
    _icons_path = Path(material.__file__).parent / "templates" / ".icons"

    _icons = {
        "*.cpp": ":simple-cplusplus:",
        "*.hpp": ":simple-cplusplus:",
        "*.c": ":simple-c:",
        "*.h": ":simple-c:",
        "*.css": ":simple-css:",
        "Dockerfile": ":simple-docker:",
        "*.fish": ":simple-fishshell:",
        "*.fs": ":simple-fsharp:",
        "*.fsi": ":simple-fsharp:",
        "*.fsx": ":simple-fsharp:",
        ".gitattributes": ":simple-git:",
        ".gitignore": ":simple-git:",
        "*.go": ":simple-go:",
        "*.gradle": ":simple-gradle:",
        "*.groovy": ":simple-apachegroovy:",
        "*.html": ":simple-html5:",
        "*.ico": ":simple-icon:",
        "*.jinja": ":simple-jinja:",
        "*.jpg": ":simple-jpeg:",
        "*.jpeg": ":simple-jpeg:",
        "*.json": ":simple-json:",
        "*.js": ":simple-javascript:",
        "*.jsx": ":simple-react:",
        "*.tsx": ":simple-react:",
        "*.kt": ":simple-kotlin:",
        "*.kts": ":simple-kotlin:",
        "*.lua": ":simple-lua:",
        "*.md": ":simple-markdown:",
        "*.odt": ":simple-libreofficewriter:",
        "*.php": ":simple-php:",
        "*.py": ":simple-python:",
        "*.pyc": ":simple-python:",
        "*.pyo": ":simple-python:",
        "*.pyd": ":simple-python:",
        "*.pyx": ":simple-python:",
        "*.rb": ":simple-ruby:",
        "*.rs": ":simple-rust:",
        "*.scala": ":simple-scala:",
        "*.scss": ":simple-sass:",
        "*.sh": ":simple-gnubash:",
        "*.svg": ":simple-svg:",
        "*.tex": ":simple-latex:",
        "*.toml": ":simple-toml:",
        "*.ts": ":simple-typescript:",
        "*.yml": ":simple-yaml:",
        "*.yaml": ":simple-yaml:",
        "*.zsh": ":simple-zsh:",
    }

    _icon_ids: dict[str | None, str] = {name: f"__ICON_{uuid4().hex}" for name in _icons.values()}
    _icon_ids[None] = f"__ICON_{uuid4().hex}"

    def _icon_to_svg(icon: str) -> str:
        return _icons_path.joinpath(*f"{icon.strip(':')}.svg".split("-", 1)).read_text(encoding="utf8")

    _svg_icons: dict[str | None, str] = {_icon_ids[value]: _icon_to_svg(value) for value in _icons.values()}
    _svg_icons[_icon_ids[None]] = _icon_to_svg(":material-file:")

    _re_icon_id = re.compile(r"__ICON_([0-9a-f]{32})")

    def _replace_icon(match: re.Match) -> str:
        return f'<span class="twemoji">{_svg_icons[match[0]]}</span>'

    def _file_icon(name: str) -> str:
        if name in _icons:
            return _icon_ids[_icons[name]]
        if (ext := f"*.{name.rsplit('.', 1)[-1]}") in _icons:
            return _icon_ids[_icons[ext]]
        return _icon_ids[None]

else:

    def _file_icon(name: str) -> str:  # noqa: ARG001
        return "📄"


def _rec_build_tree(lines: list[str], parent: list, offset: int, base_indent: int) -> int:
    while offset < len(lines):
        line = lines[offset]
        lstripped = line.lstrip()
        indent = len(line) - len(lstripped)
        if indent == base_indent:
            parent.append((lstripped, []))
            offset += 1
        elif indent > base_indent:
            offset = _rec_build_tree(lines, parent[-1][1], offset, indent)
        else:
            return offset
    return offset


def _build_tree(code: str) -> list[tuple[str, list]]:
    lines = dedent(code.strip()).split("\n")
    root_layer: list[tuple[str, list]] = []
    _rec_build_tree(lines, root_layer, 0, 0)
    return root_layer


def _rec_format_tree(tree: list[tuple[str, list]], *, root: bool = True, icons: str = "auto") -> list[str]:
    lines = []
    n_items = len(tree)
    folder_icon = "" if icons == "none" else "📁 "
    for index, node in enumerate(tree):
        last = index == n_items - 1
        prefix = "" if root else f"{'└' if last else '├'}── "
        if node[1]:
            lines.append(f"{prefix}{folder_icon}{node[0]}")
            sublines = _rec_format_tree(node[1], root=False, icons=icons)
            if root:
                lines.extend(sublines)
            else:
                indent_char = " " if last else "│"
                lines.extend([f"{indent_char}   {line}" for line in sublines])
        else:
            name = node[0].split()[0]
            icon = (
                ""
                if icons == "none"
                else folder_icon
                if name.endswith("/")
                else f"{_file_icon(name)} "
                if icons != "basic"
                else "📄 "
            )
            lines.append(f"{prefix}{icon}{node[0]}")
    return lines


def _format_tree(code: str, md: Markdown, result: str, extra: dict, **options: Any) -> str:  # noqa: ARG001
    markdown = MarkdownConverter(md)
    icons = extra.pop("icons", "auto")
    output = "\n".join(_rec_format_tree(_build_tree(code), icons=icons))
    converted = markdown.convert(code_block(result or "bash", output, **extra))
    if icons != "basic" and material is not None:
        return Markup(_re_icon_id.sub(_replace_icon, str(converted)))  # noqa: S704
    return converted
