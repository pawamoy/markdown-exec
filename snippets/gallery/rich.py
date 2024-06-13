import os

from rich.console import Console
from rich.padding import Padding
from rich.syntax import Syntax

# Here we hardcode the code snippet we want to render,
# but we could instead include it from somewhere else using the `pymdownx.snippets` extension
# (https://facelessuser.github.io/pymdown-extensions/extensions/snippets/)
# or by reading it dynamically from Python.
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

# We prevent Rich from actually writing to the terminal.
with open(os.devnull, "w") as devnull:
    console = Console(record=True, width=65, file=devnull, markup=False)
    renderable = Syntax(code, "python", theme="material")
    renderable = Padding(renderable, (0,), expand=False)
    console.print(renderable, markup=False)
svg = console.export_svg(title="async context manager")

# Wrapping the SVG in a div prevents it from being wrapped in a paragraph,
# which would add unnecessary space around it.
print(f"<div>{svg}</div>")
