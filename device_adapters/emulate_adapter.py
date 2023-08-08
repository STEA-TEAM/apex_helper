from ctypes import windll
from functools import reduce
from overrides import final
from pynput import keyboard
from typing import cast, List

from structures import TaskerBase

from .types import DeviceEvent, DeviceType, KeyboardEvent, MouseEvent, DeviceInstruction


class EmulateAdapter(TaskerBase[List[DeviceInstruction]]):
    def _abort_task(self) -> None:
        pass

    def _start_task(self, payload: List[DeviceInstruction]) -> None:
        for index, (device_type, device_event, delay) in enumerate(payload):
            print(f"Processing {device_type} event: {device_event} with delay {delay}")
            if device_type == DeviceType.Mouse:
                (event_flags, point, data) = cast(MouseEvent, device_event)
                windll.user32.mouse_event(reduce(lambda x, y: x | y, event_flags), point[0], point[1], data, 0)
            elif device_type == DeviceType.Keyboard:
            self.process(device_type, device_event)
            if index < len(payload) - 1:
                sleep(delay)
        pass

    def __init__(self):
        self.__keyboard: keyboard.Controller = keyboard.Controller()

        super().__init__()

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
