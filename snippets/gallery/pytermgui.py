import os  # markdown-exec: hide
for envvar in ("PYTHON_VERSIONS", "CI", "MULTIRUN"):  # markdown-exec: hide
    if envvar in os.environ:  # markdown-exec: hide
        print(  # markdown-exec: hide
            "PyTermGUI blocks when querying the terminal foreground color with an ANSI sequence "  # markdown-exec: hide
            "because we capture the output ourselves through `failprint`, "  # markdown-exec: hide
            "so this gallery example is disabled in CI.",  # markdown-exec: hide
        )  # markdown-exec: hide
        raise SystemExit(0)  # markdown-exec: hide
from io import StringIO

import pytermgui as ptg

code = """
    from contextlib import asynccontextmanager
    import httpx


    class BookClient(httpx.AsyncClient):
        async def get_book(self, book_id: int) -> str:
            response = await self.get(f"/books/{book_id}")
            return response.text


    @asynccontextmanager
    async def book_client(*args, **kwargs):
        async with BookClient(*args, **kwargs) as client:
            yield client
"""

terminal = ptg.Terminal(stream=StringIO(), size=(80, 16))
ptg.set_global_terminal(terminal)
with terminal.record() as recorder:
    recorder.write(ptg.tim.parse(ptg.highlight_python(code)))
svg = recorder.export_svg(inline_styles=True)

# Wrapping the SVG in a div prevents it from being wrapped in a paragraph,
# which would add unnecessary space around it.
print(f"<div>{svg}</div>")
