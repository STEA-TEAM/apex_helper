from abc import ABC, abstractmethod
from overrides import final
from threading import Thread
from time import sleep
from typing import List, LiteralString

from .types import DeviceEvent, DeviceType, DeviceInstruction


class BaseAdapter(ABC):
    def __init__(self, name: LiteralString):
        self.__instructions: List[DeviceInstruction] = []
        self.__is_running: bool = False
        self.__name: LiteralString = name
        self.__thread_handle: Thread = Thread(target=self.__consume)

        self.__thread_handle.start()

    @final
    def name(self) -> LiteralString:
        return self.__name

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
        self.__instructions = []

    def push_events(self, events: List[DeviceEvent]) -> None:
        self.__instructions += events

    def replace_events(self, events: List[DeviceEvent], force: bool) -> None:
        self.__instructions = events if force else [self.__instructions[0]] + events

    @abstractmethod
    def process(self, device_type: DeviceType, device_event: DeviceEvent) -> None:
        pass

    def __consume(self) -> None:
        while True:
            if (not self.__is_running) or len(self.__instructions) == 0:
                sleep(0.01)
                continue
            while len(self.__instructions) > 0:
                (current_device_type, current_device_event, delay) = self.__instructions[0]
                print(f"Processing {current_device_type} event: {current_device_event} with delay {delay}")
                self.process(current_device_type, current_device_event)
                sleep(delay)
                self.__instructions.pop(0)
