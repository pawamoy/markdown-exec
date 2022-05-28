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
print(recorder.export_svg(inline_styles=True))
