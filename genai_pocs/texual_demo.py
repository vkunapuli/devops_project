from textual.app import App, ComposeResult
from textual.widgets import Button, Label

class HelloWorld(App):
    def compose(self) -> ComposeResult:
            yield Label("Hello Textual")
            yield Button("Close", id="close")

    def on_button_pressed(self, event: Button.Pressed) -> None:
            if event.button.id == "close":
                self.exit()

if __name__ == "__main__":
        print('test')
        app = HelloWorld()
        app.run()
