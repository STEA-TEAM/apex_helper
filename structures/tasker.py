from abc import ABC, abstractmethod
from typing import Generic, LiteralString, TypeVar, Dict

from overrides import EnforceOverrides, final

TaskerPayloadType = TypeVar("TaskerPayloadType")
T = TypeVar("T")


class TaskerBase(ABC, EnforceOverrides, Generic[TaskerPayloadType]):
    __name: LiteralString
    __is_running: bool = False

    def __init__(self, name: LiteralString):
        self.__name = name

    def name(self) -> LiteralString:
        return self.__name

    @final
    def abort(self) -> None:
        if self.__is_running:
            self._abort_task()
            self.__is_running = False

    @final
    def restart(self, payload: TaskerPayloadType) -> None:
        self.abort()
        self.start(payload)

    @final
    def start(self, payload: TaskerPayloadType) -> None:
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
    def _start_task(self, payload: TaskerPayloadType) -> None:
        pass


class TaskerManagerBase(EnforceOverrides, Generic[T]):
    _tasker_map: Dict[LiteralString, TaskerBase] = {}

    @final
    def add_tasker(self, tasker: TaskerBase) -> None:
        if tasker.name() in self._tasker_map:
            self.remove_tasker(tasker.name())
        self._tasker_map[tasker.name()] = tasker

    @final
    def remove_tasker(self, name: LiteralString) -> None:
        if name in self._tasker_map:
            self._tasker_map[name].abort()
            del self._tasker_map[name]

    @final
    def _abort_tasks(self) -> None:
        for tasker in self._tasker_map.values():
            tasker.abort()

    @final
    def _restart_tasks(self, payload: T) -> None:
        for tasker in self._tasker_map.values():
            tasker.restart(payload)

    @final
    def _start_tasks(self, payload: T) -> None:
        for tasker in self._tasker_map.values():
            tasker.start(payload)
