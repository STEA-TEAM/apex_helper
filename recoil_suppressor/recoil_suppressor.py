from input_pubsub import InputEvent, InputSubscriber, InputType
from typing import Dict, LiteralString
from weapon_factory import WeaponSubscriber

from device_adapters import BaseAdapter


class RecoilSuppressor(InputSubscriber, WeaponSubscriber):
    __adapters: Dict[LiteralString, BaseAdapter] = {}

    def __init__(self):
        super().__init__(self.__class__.__name__)

    def register(self, adapter: BaseAdapter) -> None:
        self.__adapters[adapter.name()] = adapter

    def unregister(self, adapter: BaseAdapter) -> None:
        del self.__adapters[adapter.name()]

    def process(self, input_type: InputType, input_event: InputEvent) -> None:
        print(f"{self.name()} received {input_type} {input_event}")
