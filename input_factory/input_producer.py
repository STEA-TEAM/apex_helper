from pynput import mouse, keyboard
from typing import Dict, LiteralString

from .input_consumer import InputConsumer
from .types import InputType


class InputProducer:
    __is_running: bool = False
    __consumer_map: Dict[LiteralString, InputConsumer] = {}
    __mouse_listener: mouse.Listener
    __keyboard_listener: keyboard.Listener

    def __init__(self):
        self.__mouse_listener = mouse.Listener(
            on_move=self.__on_move,
            on_click=self.__on_click,
            on_scroll=self.__on_scroll
        )
        self.__keyboard_listener = keyboard.Listener(
            on_press=self.__on_press,
            on_release=self.__on_release
        )
        self.__mouse_listener.start()
        self.__keyboard_listener.start()

    def start(self) -> None:
        if self.__is_running:
            print(f"{self.__class__.__name__} is already running")
            return
        for consumer in self.__consumer_map.values():
            consumer.start()
        self.__is_running = True

    def stop(self) -> None:
        if not self.__is_running:
            print(f"{self.__class__.__name__} is not running")
            return

        print("Stopping Producer...")
        self.__is_running = False
        print("Stopping Consumers...")
        for consumer in self.__consumer_map.values():
            consumer.stop()

    def __on_move(self, x, y):
        if not self.__is_running:
            return
        for consumer in self.__consumer_map.values():
            consumer.feed(InputType.MouseMove, {"x": x, "y": y})

    def __on_click(self, x, y, button, pressed):
        if not self.__is_running:
            return
        for consumer in self.__consumer_map.values():
            consumer.feed(InputType.MouseClick, {"x": x, "y": y, "button": button, "pressed": pressed})

    def __on_scroll(self, x, y, dx, dy):
        if not self.__is_running:
            return
        for consumer in self.__consumer_map.values():
            consumer.feed(InputType.MouseScroll, {"x": x, "y": y, "dx": dx, "dy": dy})

    def __on_press(self, key):
        if not self.__is_running:
            return
        for consumer in self.__consumer_map.values():
            consumer.feed(InputType.KeyPress, {"key": key})

    def __on_release(self, key):
        if not self.__is_running:
            return
        for consumer in self.__consumer_map.values():
            consumer.feed(InputType.KeyRelease, {"key": key})
