from overrides import final, override
from pynput import mouse, keyboard

from structures import TaskerManagerBase, ConsumerBase
from .types import InputPayload, InputType


class InputHandler(ConsumerBase[InputPayload], TaskerManagerBase[InputPayload]):
    def __init__(self):
        self.__keyboard_listener: keyboard.Listener = keyboard.Listener(
            on_press=self.__on_press,
            on_release=self.__on_release,
        )
        self.__mouse_listener: mouse.Listener = mouse.Listener(
            on_click=self.__on_click,
            on_scroll=self.__on_scroll,
        )

        ConsumerBase.__init__(self)
        TaskerManagerBase.__init__(self)

    @final
    @override
    def _run_after_loop(self) -> None:
        self.__keyboard_listener.stop()
        self.__mouse_listener.stop()
        self._abort_tasks()

    @final
    @override
    def _run_before_loop(self) -> None:
        self.__keyboard_listener.start()
        self.__mouse_listener.start()

    @final
    @override
    def _process(self, item: InputPayload) -> None:
        self._restart_tasks(item)

    @final
    def __on_click(self, x, y, button, pressed):
        if not self._is_running():
            return
        self.append(
            (
                InputType.MouseClick,
                {"x": x, "y": y, "button": button, "pressed": pressed},
            )
        )

    @final
    def __on_scroll(self, x, y, dx, dy):
        if not self._is_running():
            return
        self.append((InputType.MouseScroll, {"x": x, "y": y, "dx": dx, "dy": dy}))

    @final
    def __on_press(self, key):
        if not self._is_running():
            return
        self.append((InputType.KeyPress, {"key": key}))

    @final
    def __on_release(self, key):
        if not self._is_running():
            return
        self.append((InputType.KeyRelease, {"key": key}))
