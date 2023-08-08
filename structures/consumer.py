from abc import abstractmethod
from queue import Queue

from overrides import override, final, EnforceOverrides
from typing import Generic, TypeVar, List, Dict, LiteralString

from .reusable_thread import ReusableThread

T = TypeVar("T")


class ConsumerBase(Generic[T], ReusableThread):
    def __init__(self):
        self.__queue: Queue[T] = Queue[T]()
        super().__init__()

    @final
    def append(self, item: T) -> None:
        self.__queue.put_nowait(item)

    @final
    def push_items(self, item_list: List[T]) -> None:
        for i in item_list:
            self.__queue.put_nowait(i)

    @final
    def replace_items(self, item_list: List[T], force: bool) -> None:
        if not force and not self.__queue.empty():
            first_item = self.__queue.get_nowait()
            self.__queue = Queue[T]()
            self.__queue.put_nowait(first_item)
            self.push_items(item_list)
        else:
            self.__queue = Queue[T]()
            self.push_items(item_list)

    @abstractmethod
    def _process(self, item: T) -> None:
        pass

    @final
    @override
    def _thread_loop(self) -> None:
        try:
            self._process(self.__queue.get())
            self.__queue.task_done()
        except IndexError:
            pass


class ConsumerManagerBase(EnforceOverrides, Generic[T]):
    def __init__(self):
        self._consumer_map: Dict[LiteralString, ConsumerBase[T]] = {}

    @final
    def add_consumer(self, consumer: ConsumerBase[T]) -> None:
        if consumer.__class__.__name__ in self._consumer_map:
            self.remove_consumer(consumer)
        self._consumer_map[consumer.__class__.__name__] = consumer

    @final
    def remove_consumer(self, consumer: ConsumerBase[T]) -> None:
        if consumer.__class__.__name__ in self._consumer_map:
            self._consumer_map[consumer.__class__.__name__].terminate()
            del self._consumer_map[consumer.__class__.__name__]

    @final
    def _append_all(self, item: T) -> None:
        for consumer in self._consumer_map.values():
            consumer.append(item)

    @final
    def _push_items_all(self, item_list: List[T]) -> None:
        for consumer in self._consumer_map.values():
            consumer.push_items(item_list)

    @final
    def _replace_items_all(self, item_list: List[T], force: bool) -> None:
        for consumer in self._consumer_map.values():
            consumer.replace_items(item_list, force)
