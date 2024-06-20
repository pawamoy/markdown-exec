"""Tests for the base formatter."""

import subprocess

import pytest
from markdown import Markdown

from markdown_exec.formatters.base import base_format


def test_no_p_around_html(md: Markdown) -> None:
    """Assert HTML isn't wrapped in a `p` tag.

    Parameters:
        md: A Markdown instance (fixture).
    """
    code = "<pre><code>hello</code></pre>"
    html = base_format(
        language="whatever",
        run=lambda code, **_: code,
        code=code,
        md=md,
        html=True,
    )
    assert html == code


@pytest.mark.parametrize("html", [True, False])
def test_render_source(md: Markdown, html: bool) -> None:
    """Assert source is rendered.

    Parameters:
        md: A Markdown instance (fixture).
        html: Whether output is HTML or not.
    """
    markup = base_format(
        language="python",
        run=lambda code, **_: code,
        code="hello",
        md=md,
        html=html,
        source="tabbed-left",
    )
    assert "Source" in markup


def test_render_console_plus_ansi_result(md: Markdown) -> None:
    """Assert we can render source as console style with `ansi` highlight.

    Parameters:
        md: A Markdown instance (fixture).
    """
    markup = base_format(
        language="bash",
        run=lambda code, **_: code,
        code="echo -e '\033[31mhello'",
        md=md,
        html=False,
        source="console",
        result="ansi",
    )
    assert "<code>ansi" in markup


def test_dont_render_anything_if_output_is_empty(md: Markdown) -> None:
    """Assert nothing is rendered if output is empty.

    Parameters:
        md: A Markdown instance (fixture).
    """
    markup = base_format(
        language="bash",
        run=lambda code, **_: "",
        code="whatever",
        md=md,
    )
    assert not markup


def test_render_source_even_if_output_is_empty(md: Markdown) -> None:
    """Assert source is rendered even if output is empty.

    Parameters:
        md: A Markdown instance (fixture).
    """
    markup = base_format(
        language="bash",
        run=lambda code, **_: "",
        code="whatever",
        md=md,
        source="tabbed-left",
    )
    assert "Source" in markup


def test_changing_working_directory(md: Markdown) -> None:
    """Assert we can change the working directory with `workdir`.

    Parameters:
        md: A Markdown instance (fixture).
    """
    markup = base_format(
        language="python",
        run=lambda code, **_: subprocess.check_output(code, shell=True, text=True),  # noqa: S602
        code="pwd",
        md=md,
        workdir="/",
    )
    assert markup == "<p>/</p>"


def test_console_width(md: Markdown) -> None:
    """Assert we can change the console width with `width`.

    Parameters:
        md: A Markdown instance (fixture).
    """
    for width in (10, 1000):
        markup = base_format(
            language="bash",
            run=lambda code, **_: subprocess.check_output(code, shell=True, text=True),  # noqa: S602,
            code="echo width: $COLUMNS",
            md=md,
            width=width,
        )
        assert f"width: {width}" in markup
