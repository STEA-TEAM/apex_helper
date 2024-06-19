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
from threading import Event
from typing import cast, List, Optional
from .utils import move_to

import math


class EnemyTracker(
    ConsumerManagerBase[DeviceInstruction],
    SubscriberBase[List[Rectangle]],
    TaskerBase[InputPayload],
):
    def __init__(self):
        screen_size = get_screen_size()
        self.__center: Point = (math.floor(screen_size.width / 2), math.floor(screen_size.height / 2))
        self.__track_event: Event = Event()
        self.ws_server: Optional = None

        ConsumerManagerBase.__init__(self)
        SubscriberBase.__init__(self)
        TaskerBase.__init__(self)

        print("EnemyTracker initialized")

    @final
    @override
    def notify(self, data: List[Rectangle]) -> None:
        if not self.__track_event.is_set():
            return
        draw_elements: List[DrawElement] = []
        if len(data) > 0:
            closest_rect = min(data, key=self.__calculate_distance)
            enemy_chest_point = (
                round((closest_rect[0][0] + closest_rect[1][0]) / 2),
                round(closest_rect[0][1] + (closest_rect[1][1] - closest_rect[0][1]) / 4)
            )
            self._append_all(move_to(self.__center, enemy_chest_point))
            if self.ws_server is not None:
                draw_elements.append({
                    "dimensions": {
                        "x1": self.__center[0],
                        "x2": enemy_chest_point[0],
                        "y1": self.__center[1],
                        "y2": enemy_chest_point[1],
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
                    self.__track_event.set()
                else:
                    self.__track_event.clear()

    def __calculate_distance(self, rect: Rectangle):
        rect_center = ((rect[0][0] + rect[1][0]) / 2, (rect[0][1] + rect[1][1]) / 2)
        return ((self.__center[0] - rect_center[0]) ** 2 + (self.__center[1] - rect_center[1]) ** 2) ** 0.5
