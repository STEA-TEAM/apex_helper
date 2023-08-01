from typing import Dict, LiteralString, cast

from overrides import override
from pynput import mouse

from device_adapters import BaseAdapter
from input_handler import InputPayload, InputType, MouseClickEvent
from structures import TaskerBase, SubscriberBase
from weapon_detector import WeaponIdentity


class RecoilSuppressor(TaskerBase[InputPayload], SubscriberBase[WeaponIdentity]):
    __adapters: Dict[LiteralString, BaseAdapter] = {}

    def __init__(self):
        super().__init__(self.__class__.__name__)

    def register(self, adapter: BaseAdapter) -> None:
        self.__adapters[adapter.name()] = adapter

    def unregister(self, adapter: BaseAdapter) -> None:
        del self.__adapters[adapter.name()]

    @override
    def _start(self, payload: InputPayload) -> None:
        (input_type, input_event) = payload
        if input_type == InputType.MouseClick:
            click_event = cast(MouseClickEvent, input_event)
            if click_event["button"] == mouse.Button.left:
                if click_event["pressed"]:
                    self.__start_recoil_suppression()
                else:
                    self.__stop_recoil_suppression()

    @override
    def abort(self) -> None:
        pass

    def __start_recoil_suppression(self) -> None:
        print(f"Try start suppressing recoil, Current weapon: {self._item}")

    def __stop_recoil_suppression(self) -> None:
        print(f"Try stop suppressing recoil, Current weapon: {self._item}")
