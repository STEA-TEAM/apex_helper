from abc import abstractmethod
from typing import Dict, Generic, LiteralString, TypeVar, List

from overrides import override, final

from .reusable_thread import ReusableThread

T = TypeVar("T")


class ConsumerBase(Generic[T], ReusableThread):
    __name: LiteralString
    __queue: List[T] = []

    def __init__(self, name: LiteralString):
        self.__name = name
        super().__init__(name)

    @final
    def append(self, item: T) -> None:
        self.__queue.append(item)

    @final
    def push_items(self, item_list: List[T]) -> None:
        self.__queue += item_list

    @final
    def replace_items(self, item_list: List[T], force: bool) -> None:
        self.__queue = item_list if force else [self.__queue[0]] + item_list

    @abstractmethod
    def _process(self, item: T) -> None:
        pass

    @final
    @override
    def _thread_loop(self) -> None:
        try:
            self._process(self.__queue.pop())
        except IndexError:
            pass