import os

from textual.app import App, ComposeResult
from textual.widgets import Static

os.environ["TEXTUAL"] = "headless"
os.environ["TEXTUAL_SCREENSHOT"] = "0.1"
os.environ["COLUMNS"] = "80"
os.environ["LINES"] = "24"

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

app = TextApp()
app.run()
print(app.export_screenshot())
