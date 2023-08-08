from abc import ABC, abstractmethod
from threading import Event, Thread

from overrides import EnforceOverrides, final


class ReusableThread(ABC, EnforceOverrides):
    def __init__(self):
        self.__run_event: Event = Event()
        self.__terminate_event: Event = Event()

        Thread(target=self.__thread_target, name=self.__class__.__name__).start()

    def start(self) -> None:
        self.__run_event.set()

    def stop(self) -> None:
        self.__run_event.clear()

    @final
    def name(self) -> str:
        return self.__class__.__name__

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
    def _is_running(self) -> bool:
        return self.__run_event.is_set()

    @final
    def __thread_target(self):
        self._run_before_loop()
        while not self.__terminate_event.is_set():
            self.__run_event.wait()
            self._thread_loop()
        self._run_after_loop()
        self.__terminate_event.clear()
