import os
from rich.console import Console
from rich.padding import Padding
from rich.syntax import Syntax

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

with open(os.devnull, "w") as devnull:
    console = Console(record=True, width=65, file=devnull, markup=False)
    renderable = Syntax(code, "python", theme="material")
    renderable = Padding(renderable, (0,), expand=False)
    console.print(renderable, markup=False)
svg = console.export_svg(title="async context manager")
print(svg)
