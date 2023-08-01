from abc import ABC, abstractmethod
from typing import Generic, LiteralString, TypeVar, Dict

from overrides import EnforceOverrides, final

T = TypeVar("T")


class TaskerBase(ABC, EnforceOverrides, Generic[T]):
    __name: LiteralString

    def __init__(self, name: LiteralString):
        self.__name = name

    def name(self) -> LiteralString:
        return self.__name

    def trigger(self, payload: T) -> None:
        self.abort()
        self._start(payload)

    @abstractmethod
    def abort(self) -> None:
        pass

    @abstractmethod
    def _start(self, payload: T) -> None:
        pass


class HandlerBase(EnforceOverrides, Generic[T]):
    __tasker_map: Dict[LiteralString, TaskerBase] = {}

    @final
    def register(self, consumer: TaskerBase) -> None:
        self.__tasker_map[consumer.name()] = consumer

    @final
    def unregister(self, name: LiteralString) -> None:
        del self.__tasker_map[name]

    @final
    def _trigger_tasks(self, payload: T) -> None:
        for tasker in self.__tasker_map.values():
            tasker.trigger(payload)

    @final
    def _abort_tasks(self) -> None:
        for tasker in self.__tasker_map.values():
            tasker.abort()
