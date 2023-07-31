from typing import Dict, Generic, LiteralString, TypeVar

T = TypeVar("T")


class SubscriberBase(Generic[T]):
    __item: T | None = None
    __name: LiteralString

    def __init__(self, name: LiteralString):
        self.__name = name
        return

    def name(self) -> LiteralString:
        return self.__name

    def notify(self, item: T) -> None:
        pass
