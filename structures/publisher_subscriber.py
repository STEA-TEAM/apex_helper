from typing import Dict, Generic, LiteralString, TypeVar

from overrides import final, EnforceOverrides

T = TypeVar("T")


class SubscriberBase(EnforceOverrides, Generic[T]):
    def __init__(self):
        self._item: T | None = None

    @final
    def notify(self, item: T) -> None:
        self._item = item


class PublisherBase(EnforceOverrides):
    def __init__(self):
        self.__subscribers: Dict[LiteralString, SubscriberBase] = {}

    @final
    def add_subscriber(self, subscriber: SubscriberBase[T]) -> None:
        self.__subscribers[subscriber.__class__.__name__] = subscriber

    @final
    def remove_subscriber(self, subscriber: SubscriberBase[T]) -> None:
        del self.__subscribers[subscriber.__class__.__name__]

    @final
    def _publish(self, item: T) -> None:
        for subscriber in self.__subscribers.values():
            subscriber.notify(item)
