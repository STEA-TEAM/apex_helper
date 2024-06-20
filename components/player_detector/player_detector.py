from overrides import override, final
from structures import (
    CV2Image,
    DrawElement,
    DrawType,
    LayerDrawServerMessage,
    Point,
    PublisherBase,
    ResultType,
    TaskerBase,
    Rectangle,
)
from typing import AnyStr, List, Optional
from ultralytics import YOLO
from utils import image_in_rectangle
from .constants import COLOR_MAPPING

import math
import numpy as np
import torch


def get_torch_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    try:
        import intel_extension_for_pytorch as ipex

        if ipex.xpu.is_available():
            return torch.device("xpu")
    except ImportError as e:
        ipex = e
        print("Error importing intel_extension_for_pytorch: ", ipex)
    return torch.device("cpu")


class PlayerDetector(TaskerBase[CV2Image], PublisherBase[List[Rectangle]]):
    def __init__(self, model_path: AnyStr, model_image_size: int = 640):
        self.ws_server: Optional = None
        self.__is_aborted: bool = False
        self.__model = YOLO(model_path, task="detect")
        self.__model_image_size: int = model_image_size

        TaskerBase.__init__(self)
        PublisherBase.__init__(self)

        print(f"PlayerDetector initialized with model image size: {model_image_size}.")

    @final
    @override
    def _abort_task(self) -> None:
        self.__is_aborted = True

    @final
    @override
    def _start_task(self, payload: CV2Image) -> None:
        self.__is_aborted = False

        offset: Point = (math.floor((payload.shape[1] - payload.shape[0]) / 2), 0)
        cropped_image = image_in_rectangle(
            payload,
            (
                offset,
                (
                    math.floor((payload.shape[1] + payload.shape[0]) / 2),
                    payload.shape[0],
                ),
            ),
        )
        if self.__is_aborted:
            return

        draw_elements: List[DrawElement] = []
        if self.ws_server is not None:
            draw_elements.append({
                "dimensions": {
                    "height": payload.shape[0],
                    "width": payload.shape[0],
                    "x": offset[0],
                    "y": offset[1],
                },
                "fill": None,
                "opacity": 0.8,
                "stroke": {
                    "color": "#9e9e9e",
                    "opacity": 1.0,
                    "width": 3,
                },
                "type": DrawType.Rectangle,
            })

        enemy_rects: List[Rectangle] = []
        for result in self.__model.predict(source=cropped_image, verbose=False):
            for box in result.boxes.cpu():
                dimension = np.floor(box.xyxy[0].numpy()).astype(int).tolist()
                class_name = self.__model.names[int(box.cls)]
                color = COLOR_MAPPING[class_name]
                if self.ws_server is not None:
                    draw_elements.append(
                        {
                            "dimensions": {
                                "height": dimension[3] - dimension[1],
                                "width": dimension[2] - dimension[0],
                                "x": offset[0] + dimension[0],
                                "y": offset[1] + dimension[1],
                            },
                            "fill": None,
                            "opacity": 0.8,
                            "stroke": {
                                "color": color,
                                "opacity": 1.0,
                                "width": 3,
                            },
                            "type": DrawType.Rectangle,
                        }
                    )
                    draw_elements.append(
                        {
                            "content": class_name,
                            "dimensions": {
                                "x": offset[0] + dimension[0],
                                "y": offset[1] + dimension[1] - 10,
                            },
                            "font": None,
                            "fill": {
                                "color": color,
                                "opacity": 1.0,
                            },
                            "opacity": 0.8,
                            "stroke": None,
                            "type": DrawType.Text,
                        }
                    )
                if class_name == "enemy":
                    enemy_rects.append(
                        (
                            (offset[0] + dimension[0], offset[1] + dimension[1]),
                            (offset[0] + dimension[2], offset[1] + dimension[3]),
                        )
                    )
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
        self._publish(enemy_rects)
