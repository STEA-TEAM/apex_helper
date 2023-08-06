from typing import Dict, Generic, LiteralString, TypeVar

from overrides import final, EnforceOverrides

T = TypeVar("T")


class SubscriberBase(EnforceOverrides, Generic[T]):
    _item: T | None = None
    __name: LiteralString

    def __init__(self, name: LiteralString):
        self.__name = name
        return

    @final
    def name(self) -> LiteralString:
        return self.__name

    @final
    def notify(self, item: T) -> None:
        self._item = item


class PublisherBase(EnforceOverrides):
    __subscribers: Dict[LiteralString, SubscriberBase] = {}

    def __init__(self):
        return

    @final
    def add_subscriber(self, subscriber: SubscriberBase[T]) -> None:
        self.__subscribers[subscriber.name()] = subscriber

    @final
    def remove_subscriber(self, subscriber: SubscriberBase[T]) -> None:
        del self.__subscribers[subscriber.name()]

    @final
    def _publish(self, item: T) -> None:
        for subscriber in self.__subscribers.values():
            subscriber.notify(item)
