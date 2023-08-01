from abc import abstractmethod
from queue import Empty, Full, Queue
from typing import Dict, Generic, LiteralString, TypeVar

from overrides import override, final

from .reusable_thread import ReusableThread

T = TypeVar("T")


class ConsumerBase(Generic[T], ReusableThread):
    __name: LiteralString
    __queue: Queue[T]

    def __init__(self, name: LiteralString, size: int = 1):
        self.__name = name
        self.__queue = Queue[T](size)
        super().__init__(name)

    @final
    def feed(self, item: T) -> None:
        try:
            self.__queue.put_nowait(item)
        except Full:
            pass

    @abstractmethod
    def _process(self, item: T) -> None:
        pass

    @final
    @override
    def _thread_loop(self) -> None:
        try:
            self._process(self.__queue.get_nowait())
        except Empty:
            pass


class ProducerBase(Generic[T], ReusableThread):
    _consumer_map: Dict[LiteralString, ConsumerBase] = {}

    @final
    @override
    def start(self) -> None:
        super().start()
        for consumer in self._consumer_map.values():
            consumer.start()

    @final
    @override
    def stop(self) -> None:
        super().stop()
        for consumer in self._consumer_map.values():
            consumer.stop()

    @final
    def register(self, consumer: ConsumerBase) -> None:
        self._consumer_map[consumer.name()] = consumer

    @final
    def unregister(self, name: LiteralString) -> None:
        del self._consumer_map[name]

    @abstractmethod
    def _produce(self) -> T:
        pass

    @override
    def _thread_loop(self) -> None:
        item = self._produce()
        for consumer in self._consumer_map.values():
            consumer.feed(item)
