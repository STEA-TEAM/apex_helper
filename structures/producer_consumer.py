from queue import PriorityQueue
from typing import Dict, Generic, LiteralString, TypeVar

T = TypeVar("T")
ConsumerType = TypeVar("ConsumerType")


class ConsumerBase(Generic[T]):
    __current: T | None = None
    __name: LiteralString
    __queue: PriorityQueue[T]

    def __init__(self, name: LiteralString, size: int = 0):
        self.__name = name
        self.__queue = PriorityQueue[T](size)


class ProducerBase(Generic[ConsumerType]):
    __consumer_map: Dict[LiteralString, ConsumerBase[ConsumerType]] = {}
