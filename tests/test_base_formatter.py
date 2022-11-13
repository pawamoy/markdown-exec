"""Tests for the base formatter."""

import pytest
from markdown import Markdown

from markdown_exec.formatters.base import base_format


def test_no_p_around_html(md: Markdown) -> None:
    """Assert HTML isn't wrapped in a `p` tag.

    Parameters:
        md: A Markdown instance (fixture).
    """
    code = "<pre><code>hello</code></pre>"
    html = base_format("whatever", lambda _: _, code, md, html=True, source="", result="", tabs=("", ""))
    assert html == code


@pytest.mark.parametrize("html", [True, False])
def test_render_source(md: Markdown, html: bool) -> None:
    """Assert source is rendered.

    Parameters:
        md: A Markdown instance (fixture).
        html: Whether output is HTML or not.
    """
    markup = base_format("python", lambda _: _, "hello", md, html, "tabbed-left", "", ("Source", "Output"))
    assert "Source" in markup
