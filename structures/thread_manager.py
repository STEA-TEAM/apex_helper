from overrides import EnforceOverrides, final
from structures import ReusableThread
from typing import AnyStr, Dict


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
