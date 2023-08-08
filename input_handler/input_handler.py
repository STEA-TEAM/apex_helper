from overrides import final
from pynput import mouse, keyboard

from structures import TaskerManagerBase
from .types import InputPayload, InputType


class InputHandler(TaskerManagerBase[InputPayload]):
    def __init__(self):
        self.__is_running: bool = False
        self.__mouse_listener: mouse.Listener = mouse.Listener(
            on_click=self.__on_click,
            on_scroll=self.__on_scroll,
        )
        self.__keyboard_listener: keyboard.Listener = keyboard.Listener(
            on_press=self.__on_press,
            on_release=self.__on_release,
        )

        super().__init__()
        self.__mouse_listener.start()
        self.__keyboard_listener.start()

    @final
    def start(self) -> None:
        if self.__is_running:
            print(f"{self.__class__.__name__} is already running")
            return
        self.__is_running = True

    @final
    def stop(self) -> None:
        if not self.__is_running:
            print(f"{self.__class__.__name__} is not running")
            return

        print("Stopping Producer...")
        self.__is_running = False
        print("Stopping Consumers...")
        self._abort_tasks()

    @final
    def terminate(self) -> None:
        self.__keyboard_listener.stop()
        self.__mouse_listener.stop()

    @final
    def __on_click(self, x, y, button, pressed):
        if not self.__is_running:
            return
        self._restart_tasks(
            (
                InputType.MouseClick,
                {"x": x, "y": y, "button": button, "pressed": pressed},
            )
        )

    @final
    def __on_scroll(self, x, y, dx, dy):
        if not self.__is_running:
            return
        self._restart_tasks(
            (InputType.MouseScroll, {"x": x, "y": y, "dx": dx, "dy": dy})
        )

    @final
    def __on_press(self, key):
        if not self.__is_running:
            return
        self._restart_tasks((InputType.KeyPress, {"key": key}))

    @final
    def __on_release(self, key):
        if not self.__is_running:
            return
        self._restart_tasks((InputType.KeyRelease, {"key": key}))
