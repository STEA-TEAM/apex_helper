from components.device_adapters import DeviceInstruction
from components.input_handler import InputPayload, InputType, MouseClickEvent
from overrides import override, final
from pynput import mouse
from structures import TaskerBase, SubscriberBase, ConsumerManagerBase
from typing import cast
from components.weapon_detector import WeaponIdentity

from .constants import RECOIL_SUPPRESSION_DICT


class RecoilSuppressor(
    TaskerBase[InputPayload],
    ConsumerManagerBase[DeviceInstruction],
    SubscriberBase[WeaponIdentity],
):
    def __init__(self):
        TaskerBase.__init__(self)
        ConsumerManagerBase.__init__(self)
        SubscriberBase.__init__(self)

        print("RecoilSuppressor initialized")

    @final
    @override
    def _abort_task(self) -> None:
        self.__stop_recoil_suppression()

    @final
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

    @final
    def __start_recoil_suppression(self) -> None:
        if self._item in RECOIL_SUPPRESSION_DICT:
            suppress_events = RECOIL_SUPPRESSION_DICT[self._item]
            self._replace_items_all(suppress_events, False)

    @final
    def __stop_recoil_suppression(self) -> None:
        self._replace_items_all([], True)
