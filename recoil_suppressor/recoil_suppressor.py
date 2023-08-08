from device_adapters import BaseAdapter
from input_handler import InputPayload, InputType, MouseClickEvent
from overrides import override
from pynput import mouse
from structures import TaskerBase, SubscriberBase
from typing import Dict, LiteralString, cast
from weapon_detector import WeaponIdentity

from .constants import RECOIL_SUPPRESSION_DICT


class RecoilSuppressor(TaskerBase[InputPayload], SubscriberBase[WeaponIdentity]):
    def __init__(self):
        self.__adapters: Dict[LiteralString, BaseAdapter] = {}
        TaskerBase.__init__(self)
        SubscriberBase.__init__(self)

    def register(self, adapter: BaseAdapter) -> None:
        self.__adapters[adapter.name()] = adapter

    def unregister(self, adapter: BaseAdapter) -> None:
        del self.__adapters[adapter.name()]

    @override
    def _abort_task(self) -> None:
        for adapter_name, adapter in self.__adapters.items():
            adapter.replace_events([], True)

    @override
    def _start_task(self, payload: InputPayload) -> None:
        (input_type, input_event) = payload
        if input_type == InputType.MouseClick:
            click_event = cast(MouseClickEvent, input_event)
            if click_event["button"] == mouse.Button.left:
                if click_event["pressed"]:
                    self.__start_recoil_suppression()
                else:
                    self.__stop_recoil_suppression()

    def __start_recoil_suppression(self) -> None:
        if self._item in RECOIL_SUPPRESSION_DICT:
            print(f"Try start suppressing recoil, Current weapon: {self._item}")
            suppress_events = RECOIL_SUPPRESSION_DICT[self._item]
            print(f"Suppress events: {suppress_events}")
            for adapter_name, adapter in self.__adapters.items():
                print(f"Pushing events to {adapter_name}")
                adapter.push_events(suppress_events)

    def __stop_recoil_suppression(self) -> None:
        print(f"Try stop suppressing recoil, Current weapon: {self._item}")
