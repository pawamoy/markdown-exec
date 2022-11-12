from textual.app import App, ComposeResult
from textual.pilot import Pilot
from textual.widgets import Static


class TextApp(App):
    CSS = """
    Screen {
        background: darkblue;
        color: white;
        layout: vertical;
    }
    Static {
        height: auto;
        padding: 2;
        border: heavy white;
        background: #ffffff 30%;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Hello")
        yield Static("[b]World![/b]")


async def auto_pilot(pilot: Pilot):
    pilot.app.exit(pilot.app.export_screenshot())


print(TextApp().run(headless=True, size=(80, 24), auto_pilot=auto_pilot))
