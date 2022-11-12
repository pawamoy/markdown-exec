"""Tests for the base formatter."""


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
