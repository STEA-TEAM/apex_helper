from abc import ABC, abstractmethod
from overrides import override, final, EnforceOverrides
from queue import PriorityQueue, Full
from typing import Dict, Generic, LiteralString, TypeVar

from .reusable_thread import ReusableThread

T = TypeVar("T")


class ConsumerBase(ABC, Generic[T], ReusableThread):
    __name: LiteralString
    __queue: PriorityQueue[T]

    def __init__(self, name: LiteralString, size: int = 0):
        self.__name = name
        self.__queue = PriorityQueue[T](size)
        super().__init__(name)

    @final
    def feed(self, item: T, priority: int = 0) -> None:
        try:
            self.__queue.put_nowait((priority, item))
        except Full:
            pass

    @abstractmethod
    def _process(self, item: T) -> None:
        pass

    @final
    @override
    def _thread_loop(self) -> None:
        if not self.__queue.empty():
            self._process(self.__queue.get())


class ProducerBase(ABC, EnforceOverrides, ReusableThread):
    __consumer_map: Dict[LiteralString, ConsumerBase] = {}

    @final
    @override
    def start(self) -> None:
        super().start()
        for consumer in self.__consumer_map.values():
            consumer.start()

    @final
    @override
    def stop(self) -> None:
        super().stop()
        for consumer in self.__consumer_map.values():
            consumer.stop()

    @final
    def register(self, consumer: ConsumerBase) -> None:
        self.__consumer_map[consumer.name()] = consumer

    @final
    def unregister(self, name: LiteralString) -> None:
        del self.__consumer_map[name]
