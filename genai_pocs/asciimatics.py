from asciimatics.screen import Screen

def demo(screen):
        screen.print_at("Hello, Asciimatics!",
                        int(screen.width / 2 - 10), int(screen.height / 2),
                        colour=Screen.COLOUR_CYAN,
                        bg=Screen.COLOUR_BLUE)
        screen.refresh()
        screen.wait_for_input()

Screen.wrapper(demo)
