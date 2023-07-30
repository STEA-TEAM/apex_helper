from abc import ABC, abstractmethod
from threading import Event, Thread
from overrides import EnforceOverrides


class ReusableThread(ABC, EnforceOverrides):
    __run_event: Event = Event()
    __terminate_event: Event = Event()

    def __init__(self):
        Thread(target=self.__thread_target).start()

    def start(self) -> None:
        self.__run_event.set()

    def stop(self) -> None:
        self.__run_event.clear()

    def terminate(self) -> None:
        self.__terminate_event.set()

    def _run_before_loop(self) -> None:
        pass

    @abstractmethod
    def _thread_loop(self) -> None:
        pass

    def _run_after_loop(self) -> None:
        pass

    def __thread_target(self):
        self._run_before_loop()
        while not self.__terminate_event.is_set():
            self.__run_event.wait()
            self._thread_loop()
        self.__terminate_event.clear()
        self._run_after_loop()
