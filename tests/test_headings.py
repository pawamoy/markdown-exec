"""Tests for headings."""

from __future__ import annotations

import os
import subprocess
import sys
from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from markdown import Markdown


def test_headings_removal(md: Markdown) -> None:
    """Headings should leave no trace behind.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            === "File layout"

                ```tree
                ./
                    hello.md
                ```
            """,
        ),
    )
    assert 'class="markdown-exec"' not in html


def test_mkdocstrings_heading_placeholders_do_not_leak_into_toc(tmp_path: Path) -> None:
    """Mkdocstrings headings with stashed inline code should not corrupt the ToC."""
    (tmp_path / "docs").mkdir()
    package = tmp_path / "repro_pkg"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf8")
    (package / "repro97.py").write_text(
        dedent(
            '''\
            """Summary.

            # Heading `1`

            Text with `code`.

            # Heading `2`

            Text with `code again`.

            # Heading `3`

            Text with `code again and again`.

            # Heading `4`.

            Text with `code again and again again`.
            """
            ''',
        ),
        encoding="utf8",
    )
    (tmp_path / "docs" / "index.md").write_text(
        dedent(
            """\
            # Executed block

            ```python exec="true" source="material-block"
            print("hello from the exec block")
            ```

            # Documented module

            ::: repro_pkg.repro97
            """,
        ),
        encoding="utf8",
    )
    (tmp_path / "mkdocs.yml").write_text(
        dedent(
            """\
            site_name: repro97
            plugins:
              - search
              - markdown-exec
              - mkdocstrings:
                  handlers:
                    python:
                      paths: [.]
            markdown_extensions:
              - toc
              - pymdownx.superfences
              - pymdownx.highlight
              - pymdownx.inlinehilite
            """,
        ),
        encoding="utf8",
    )
    env = os.environ | {
        "PYTHONPATH": os.pathsep.join(
            path for path in (str(tmp_path), os.environ.get("PYTHONPATH", "")) if path
        ),
    }

    result = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "-q"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    html = (tmp_path / "site" / "index.html").read_text(encoding="utf8")
    assert "wzxhzdk" not in html
    assert "Heading 1</a>" in html
    assert "Heading 2</a>" in html
    assert "Heading 3</a>" in html
    assert "Heading 4.</a>" in html
    assert "Heading print(&quot;hello from the exec block&quot;)" not in html
