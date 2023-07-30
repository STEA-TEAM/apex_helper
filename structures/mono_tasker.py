from abc import ABC, abstractmethod
from typing import Generic, LiteralString, TypeVar

T = TypeVar("T")


class MonoTasker(ABC, Generic[T]):
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
