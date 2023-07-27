from abc import ABC, abstractmethod
from threading import Thread
from time import sleep
from typing import List, LiteralString, Tuple

from .types import DeviceEvent, DeviceType


class BaseAdapter(ABC):
    __events: List[Tuple[DeviceType, DeviceEvent, float]] = []
    __is_running: bool = False
    __name: LiteralString
    __thread_handle: Thread

    def __init__(self, name: LiteralString):
        self.__name = name
        self.__thread_handle = Thread(target=self.__consume)
        self.__thread_handle.start()

    def start(self) -> None:
        if self.__is_running:
            print(f"{self.__class__.__name__} is already running")
            return
        print(f"Starting {self.__class__.__name__}...")
        self.__is_running = True

    def stop(self) -> None:
        if not self.__is_running:
            print(f"{self.__class__.__name__} is not running")
            return
        print(f"Stopping {self.__class__.__name__}...")
        self.__is_running = False
        self.__events = []

    def push_events(self, events: List[Tuple[DeviceType, DeviceEvent, float]]) -> None:
        self.__events += events

    def replace_events(self, events: List[Tuple[DeviceType, DeviceEvent, float]], force: bool) -> None:
        self.__events = events if force else [self.__events[0]] + events

    @abstractmethod
    def process(self, device_type: DeviceType, device_event: DeviceEvent) -> None:
        pass

    def __consume(self) -> None:
        while True:
            if (not self.__is_running) or len(self.__events) == 0:
                sleep(0.01)
                continue
            while len(self.__events) > 0:
                (current_device_type, current_device_event, delay) = self.__events[0]
                self.process(current_device_type, current_device_event)
                sleep(delay)
                self.__events.pop(0)
