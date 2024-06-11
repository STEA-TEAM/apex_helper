from components.device_adapters import DeviceInstruction
from components.input_handler import InputPayload, InputType, MouseClickEvent
from overrides import final, override
from pyautogui import size as get_screen_size
from pynput import mouse
from structures import (
    ConsumerManagerBase,
    DrawElement,
    DrawType,
    LayerDrawServerMessage,
    Point,
    Rectangle,
    ResultType,
    SubscriberBase,
    TaskerBase,
)
from typing import cast, List, Optional

import math


class EnemyTracker(
    TaskerBase[InputPayload],
    ConsumerManagerBase[DeviceInstruction],
    SubscriberBase[List[Rectangle]],
):
    def __init__(self):
        screen_size = get_screen_size()
        self.__center: Point = (math.floor(screen_size.width / 2), math.floor(screen_size.height / 2))
        self.ws_server: Optional = None

        TaskerBase.__init__(self)
        ConsumerManagerBase.__init__(self)
        SubscriberBase.__init__(self)

        print("EnemyTracker initialized")

    @final
    @override
    def _abort_task(self) -> None:
        pass

    @final
    @override
    def _start_task(self, payload: InputPayload) -> None:
        (input_type, input_event) = payload
        if input_type == InputType.MouseClick:
            click_event = cast(MouseClickEvent, input_event)
            if click_event["button"] == mouse.Button.right:
                if click_event["pressed"]:
                    self.__start_tracking()
                else:
                    self.__stop_tracking()

    @final
    def __start_tracking(self) -> None:
        draw_elements: List[DrawElement] = []
        if self._item is not None:
            closest_rect = min(self._item, key=self.__calculate_distance)
            if self.ws_server is not None:
                draw_elements.append({
                    "dimensions": {
                        "x1": self.__center[0],
                        "x2": (closest_rect[0][0] + closest_rect[1][0]) / 2,
                        "y1": self.__center[1],
                        "y2": closest_rect[0][1] + (closest_rect[1][1] - closest_rect[0][1]) / 4,
                    },
                    "fill": None,
                    "opacity": 0.8,
                    "stroke": {
                        "color": "#00bcd4",
                        "opacity": 1.0,
                        "width": 3,
                    },
                    "type": DrawType.Line,
                })
        if self.ws_server is not None:
            self.ws_server.broadcast(
                LayerDrawServerMessage(
                    {
                        "elements": draw_elements,
                        "message": None,
                        "name": self.__class__.__name__,
                        "result": ResultType.success,
                    }
                )
            )

    @final
    def __stop_tracking(self) -> None:
        if self.ws_server is not None:
            self.ws_server.broadcast(
                LayerDrawServerMessage(
                    {
                        "elements": [],
                        "message": None,
                        "name": self.__class__.__name__,
                        "result": ResultType.success,
                    }
                )
            )

    def __calculate_distance(self, rect: Rectangle):
        rect_center = ((rect[0][0] + rect[1][0]) / 2, (rect[0][1] + rect[1][1]) / 2)
        return ((self.__center[0] - rect_center[0]) ** 2 + (self.__center[1] - rect_center[1]) ** 2) ** 0.5
