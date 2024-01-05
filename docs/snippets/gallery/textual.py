from textual.app import App, ComposeResult
from textual.widgets import Static
from textual._doc import take_svg_screenshot


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


print(take_svg_screenshot(app=TextApp(), terminal_size=(80, 24)))
