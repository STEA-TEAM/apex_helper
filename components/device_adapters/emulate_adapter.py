from ctypes import windll
from functools import reduce
from overrides import final, override
from pynput import keyboard
from time import sleep
from structures import ConsumerBase
from typing import cast

from .types import DeviceType, KeyboardEvent, MouseEvent, DeviceInstruction


class EmulateAdapter(ConsumerBase[DeviceInstruction]):
    def __init__(self):
        self.__keyboard: keyboard.Controller = keyboard.Controller()

        super().__init__()

        print("EmulateAdapter initialized")

    @final
    @override
    def _process(self, item: DeviceInstruction) -> None:
        (device_type, device_event, delay) = item
        if device_type == DeviceType.Mouse:
            (event_flags, point, data) = cast(MouseEvent, device_event)
            windll.user32.mouse_event(
                reduce(lambda x, y: x | y, event_flags), point[0], point[1], data, 0
            )
        elif device_type == DeviceType.Keyboard:
            for key_states in cast(KeyboardEvent, device_event):
                (key, is_pressed) = key_states
                if is_pressed:
                    self.__keyboard.press(key)
                else:
                    self.__keyboard.release(key)
        sleep(delay)
