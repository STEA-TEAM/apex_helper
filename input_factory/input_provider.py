from pynput import mouse


class InputProvider:
    __mouse_listener: mouse.Listener

    def __init__(self):
        __mouse_listener = mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll
        )
