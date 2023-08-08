from abc import abstractmethod
from overrides import override, final, EnforceOverrides
from queue import Queue, Empty
from threading import Lock
from typing import Generic, TypeVar, List, Dict, LiteralString

from .reusable_thread import ReusableThread

T = TypeVar("T")


class ConsumerBase(Generic[T], ReusableThread):
    def __init__(self):
        self.__queue: Queue[T] = Queue[T]()
        self.__queue_lock: Lock = Lock()
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
        self.__queue_lock.acquire()
        try:
            first_item = self.__queue.get_nowait()
        except Empty:
            first_item = None
        self.__clear_queue()
        if not force and Empty is not None:
            self.append(first_item)
        self.push_items(item_list)
        self.__queue_lock.release()

    @abstractmethod
    def _process(self, item: T) -> None:
        pass

    @final
    @override
    def _thread_loop(self) -> None:
        try:
            item = self.__queue.get(timeout=0.1)
            if item is not None:
                self._process(item)
            self.__queue.task_done()
        except (Empty, ValueError):
            pass

    @final
    @override
    def _run_after_loop(self) -> None:
        print(f"Consumer {self.__class__.__name__} terminated")

    def __clear_queue(self) -> None:
        while not self.__queue.empty():
            try:
                self.__queue.get_nowait()
            except Empty:
                continue
            self.__queue.task_done()


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
