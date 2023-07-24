from abc import ABC, abstractmethod
from numpy import ndarray as opencv_image
from threading import Event, Thread
from time import sleep
from typing import LiteralString


class ImageConsumer(ABC):
    _current_image: opencv_image | None = None
    __name: LiteralString
    __stop_event: Event = Event()
    __thread_handle: Thread

    def __init__(self, name: LiteralString):
        self.__name = name
        self.__thread_handle = Thread(target=self.__run)
        return

    def name(self) -> LiteralString:
        return self.__name

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

    def feed(self, image: opencv_image) -> None:
        self._current_image = image

    @abstractmethod
    def process(self) -> None:
        pass

    def __run(self) -> None:
        while True:
            if self.__stop_event.is_set():
                break
            if self._current_image is not None:
                self.process()
            else:
                sleep(0.001)
        self.__stop_event.clear()
