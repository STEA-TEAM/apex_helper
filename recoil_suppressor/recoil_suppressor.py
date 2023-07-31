from typing import Dict, LiteralString

from device_adapters import BaseAdapter
from input_handler import InputPayload
from structures import MonoTasker
from weapon_pubsub import WeaponSubscriber


class RecoilSuppressor(MonoTasker[InputPayload], WeaponSubscriber):
    def _start(self, payload: InputPayload) -> None:
        (input_type, input_event) = payload
        # print(f"{self.name()} received {input_type} {input_event}")

    def abort(self) -> None:
        pass

    __adapters: Dict[LiteralString, BaseAdapter] = {}

    def __init__(self):
        MonoTasker.__init__(self, self.__class__.__name__)
        WeaponSubscriber.__init__(self, self.__class__.__name__)

    def register(self, adapter: BaseAdapter) -> None:
        self.__adapters[adapter.name()] = adapter

    def unregister(self, adapter: BaseAdapter) -> None:
        del self.__adapters[adapter.name()]
