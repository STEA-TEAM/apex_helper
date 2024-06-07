from abc import ABC, abstractmethod
from overrides import EnforceOverrides, final
from threading import Event, Thread
from typing import AnyStr, Dict


class ReusableThread(ABC, EnforceOverrides):
    def __init__(self):
        self.__run_event: Event = Event()
        self.__terminate_event: Event = Event()

        thread_manager.register(self)

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


class ThreadManager(EnforceOverrides):
    def __init__(self):
        self._thread_map: Dict[AnyStr, ReusableThread] = {}

    @final
    def register(self, reusable_thread: ReusableThread) -> "ThreadManager":
        if reusable_thread.name() not in self._thread_map:
            self.unregister(reusable_thread)
        self._thread_map[reusable_thread.name()] = reusable_thread
        return self

    @final
    def unregister(self, reusable_thread: ReusableThread) -> "ThreadManager":
        if reusable_thread.name() in self._thread_map:
            self._thread_map[reusable_thread.name()].terminate()
            del self._thread_map[reusable_thread.name()]
        return self

    @final
    def start(self) -> "ThreadManager":
        print(
            f"Starting {self._thread_map.__len__()} threads: {', '.join(self._thread_map.keys())}"
        )
        for reusable_thread in self._thread_map.values():
            reusable_thread.start()
        return self

    @final
    def stop(self) -> "ThreadManager":
        for reusable_thread in self._thread_map.values():
            reusable_thread.stop()
        return self

    @final
    def terminate(self) -> "ThreadManager":
        for reusable_thread in self._thread_map.values():
            reusable_thread.terminate()
        return self


thread_manager = ThreadManager()
