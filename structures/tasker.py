from abc import ABC, abstractmethod
from typing import Generic, LiteralString, TypeVar, Dict

from overrides import EnforceOverrides, final

PayloadType = TypeVar("PayloadType")


class TaskerBase(ABC, EnforceOverrides, Generic[PayloadType]):
    def __init__(self):
        self.__is_running: bool = False

    @final
    def abort(self) -> None:
        if self.__is_running:
            self._abort_task()
            self.__is_running = False

    @final
    def restart(self, payload: PayloadType) -> None:
        self.abort()
        self.start(payload)

    @final
    def start(self, payload: PayloadType) -> None:
        if self.__is_running:
            print(f"{self.__class__.__name__} is already running")
            return
        self.__is_running = True
        self._start_task(payload)
        self.__is_running = False

    @abstractmethod
    def _abort_task(self) -> None:
        pass

    @abstractmethod
    def _start_task(self, payload: PayloadType) -> None:
        pass


class TaskerManagerBase(Generic[PayloadType]):
    def __init__(self):
        self._tasker_map: Dict[LiteralString, TaskerBase[PayloadType]] = {}

    @final
    def add_tasker(self, tasker: TaskerBase[PayloadType]) -> None:
        if tasker.__class__.__name__ in self._tasker_map:
            self.remove_tasker(tasker)
        self._tasker_map[tasker.__class__.__name__] = tasker

    @final
    def remove_tasker(self, tasker: TaskerBase[PayloadType]) -> None:
        if tasker.__class__.__name__ in self._tasker_map:
            self._tasker_map[tasker.__class__.__name__].abort()
            del self._tasker_map[tasker.__class__.__name__]

    @final
    def _abort_tasks(self) -> None:
        for tasker in self._tasker_map.values():
            tasker.abort()

    @final
    def _restart_tasks(self, payload: PayloadType) -> None:
        for tasker in self._tasker_map.values():
            tasker.restart(payload)

    @final
    def _start_tasks(self, payload: PayloadType) -> None:
        for tasker in self._tasker_map.values():
            tasker.start(payload)
