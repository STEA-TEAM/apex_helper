from abc import abstractmethod
from typing import Dict, Generic, AnyStr, TypeVar

from overrides import final, EnforceOverrides

T = TypeVar("T")


class SubscriberBase(EnforceOverrides, Generic[T]):
    @abstractmethod
    def notify(self, data: T) -> None:
        pass


class PublisherBase(EnforceOverrides, Generic[T]):
    def __init__(self):
        self.__subscribers: Dict[AnyStr, SubscriberBase] = {}

    @final
    def add_subscriber(self, subscriber: SubscriberBase[T]) -> None:
        self.__subscribers[subscriber.__class__.__name__] = subscriber

    @final
    def remove_subscriber(self, subscriber: SubscriberBase[T]) -> None:
        del self.__subscribers[subscriber.__class__.__name__]

    @final
    def _publish(self, data: T) -> None:
        for subscriber in self.__subscribers.values():
            subscriber.notify(data)
