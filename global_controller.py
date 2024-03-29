from pynput import keyboard
from typing import Dict, LiteralString


class GlobalController:
    __keyboard_listener: keyboard.Listener
    __thread_map: Dict[LiteralString, Thread] = {}

    def __init__(self):
        self.__keyboard_listener = keyboard.Listener(
            on_press=self.__on_press,
            on_release=self.__on_release
        )
        self.__mouse_listener.start()
        self.__keyboard_listener.start()

    def __on_press(self, key):
        if key == Key.delete:
            image_producer.stop()
            return