from abc import ABC, abstractmethod
from threading import Thread
from typing import LiteralString

from .types import InputEvent, InputType


class InputSubscriber(ABC):
    __current_task: Thread | None = None
    __name: LiteralString

    def __init__(self, name: LiteralString):
        self.__name = name

    def abort(self) -> None:
        if self.__current_task is None or not self.__current_task.is_alive():
            return
        print(f"Aborting {self.__name}'s active task...")
        self.__current_task.join(0)

    def notify(self, input_type: InputType, input_event: InputEvent) -> None:
        self.abort()
        self.__current_task = Thread(target=self.process, args=(input_type, input_event))
        self.__current_task.start()

    @abstractmethod
    def process(self, input_type: InputType, input_event: InputEvent) -> None:
        pass
