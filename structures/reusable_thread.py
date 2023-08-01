from abc import ABC, abstractmethod
from threading import Event, Thread
from typing import LiteralString, final

from overrides import EnforceOverrides


class ReusableThread(ABC, EnforceOverrides):
    __name: LiteralString
    __run_event: Event = Event()
    __terminate_event: Event = Event()

    def __init__(self, name: LiteralString):
        self.__name = name
        Thread(target=self.__thread_target).start()

    @final
    def name(self) -> LiteralString:
        return self.__name

    def start(self) -> None:
        self.__run_event.set()

    def stop(self) -> None:
        self.__run_event.clear()

    @final
    def terminate(self) -> None:
        self.__terminate_event.set()

    @abstractmethod
    def _thread_loop(self) -> None:
        pass

    def _run_before_loop(self) -> None:
        pass

    def _run_after_loop(self) -> None:
        pass

    @final
    def __thread_target(self):
        self._run_before_loop()
        while not self.__terminate_event.is_set():
            self.__run_event.wait()
            self._thread_loop()
        self._run_after_loop()
        self.__terminate_event.clear()
