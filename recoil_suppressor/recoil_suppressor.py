from input_factory import InputConsumer
from typing import Dict, LiteralString
from weapon_factory import WeaponSubscriber

from device_adapters import BaseAdapter


class RecoilSuppressor(InputConsumer, WeaponSubscriber):
    __adapters: Dict[LiteralString, BaseAdapter] = {}

    def __init__(self):
        super().__init__(self.__class__.__name__)

    def process(self) -> None:
        pass
