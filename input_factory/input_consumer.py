from abc import ABC, abstractmethod
from threading import Event, Thread
from time import sleep
from typing import LiteralString

from .types import InputEvent


class InputConsumer(ABC):
    _current_input_event: InputEvent | None = None
    __name: LiteralString
    __stop_event: Event = Event()
    __thread_handle: Thread

    def __init__(self, name: LiteralString):
        self.__name = name
        self.__thread_handle = Thread(target=self.__run)

    def start(self) -> None:
        if self.__thread_handle.is_alive():
            print(f"{self.__name} is already running")
            return
        print(f"Starting {self.__name}...")
        self.__thread_handle.start()

    def stop(self) -> None:
        if not self.__thread_handle.is_alive():
            print(f"{self.__name} is not running")
            return
        print(f"Stopping {self.__name}...")
        self.__stop_event.set()
        self.__thread_handle.join()

    def feed(self, input_event: InputEvent) -> None:
        self._current_input_event = input_event

    @abstractmethod
    def process(self) -> None:
        pass

    def __run(self) -> None:
        while True:
            if self.__stop_event.is_set():
                break
            if self._current_input_event is not None:
                self.process()
            else:
                sleep(0.001)
        self.__stop_event.clear()
