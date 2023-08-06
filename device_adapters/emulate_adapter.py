from ctypes import windll
from functools import reduce
from overrides import final
from pynput import keyboard
from typing import cast

from .base_adapter import BaseAdapter
from .types import DeviceEvent, DeviceType, KeyboardEvent, MouseEvent


class EmulateAdapter(BaseAdapter):
    __keyboard: keyboard.Controller = keyboard.Controller()

    def __init__(self):
        super().__init__(self.__class__.__name__)

    @final
    def process(self, device_type: DeviceType, device_event: DeviceEvent) -> None:
        if device_type == DeviceType.Mouse:
            (event_flags, point, data) = cast(MouseEvent, device_event)
            windll.user32.mouse_event(reduce(lambda x, y: x | y, event_flags), point[0], point[1], data, 0)
        elif device_type == DeviceType.Keyboard:
            for key_states in cast(KeyboardEvent, device_event):
                (key, is_pressed) = key_states
                if is_pressed:
                    self.__keyboard.press(key)
                else:
                    self.__keyboard.release(key)
