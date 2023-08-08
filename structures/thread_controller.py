from overrides import EnforceOverrides, final
from structures import ReusableThread
from typing import Dict, LiteralString


class ThreadController(EnforceOverrides):
    def __init__(self):
        self._thread_map: Dict[LiteralString, ReusableThread] = {}

    @final
    def register(self, reusable_thread: ReusableThread):
        self._thread_map[reusable_thread.name()] = reusable_thread

    @final
    def start(self):
        for reusable_thread in self._thread_map.values():
            reusable_thread.start()

    @final
    def stop(self):
        for reusable_thread in self._thread_map.values():
            reusable_thread.stop()

    @final
    def terminate(self):
        for reusable_thread in self._thread_map.values():
            reusable_thread.terminate()


thread_controller = ThreadController()
