from numpy import floor
from overrides import override, final
from structures import (
    CV2Image,
    ImageEditor,
    NdiHelper,
    PublisherBase,
    TaskerBase,
    Point,
)
from typing import AnyStr
from ultralytics import YOLO
from utils import image_in_rectangle

import cv2
import math
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


class PlayerDetector(TaskerBase[CV2Image], PublisherBase):
    def __init__(self, model_path: AnyStr, model_image_size: int = 640):
        self.__is_aborted: bool = False
        self.__model = YOLO(model_path).to(get_torch_device())
        self.__model_image_size: int = model_image_size
        self.__ndi_helper: NdiHelper = NdiHelper("PlayerDetector")

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

        image_editor = ImageEditor(cv2.cvtColor(payload, cv2.COLOR_BGR2BGRA))
        image_editor.add_rectangle(
            (
                offset,
                (
                    math.floor((payload.shape[1] + payload.shape[0]) / 2),
                    payload.shape[0],
                ),
            ),
            (255, 255, 255, 127)
        )

        for result in self.__model.predict(source=cropped_image, verbose=False):
            for box in result.boxes.cpu():
                dimension = floor(box.xyxy[0].numpy()).astype(int)
                class_name = self.__model.names[int(box.cls)]
                image_editor.add_rectangle(
                    (
                        (offset[0] + dimension[0], offset[1] + dimension[1]),
                        (offset[0] + dimension[2], offset[1] + dimension[3]),
                    ),
                    class_name == "allies" and (0, 255, 0, 255) or (0, 0, 255, 255),
                )
                image_editor.add_text(
                    class_name,
                    (offset[0] + dimension[0], offset[1] + dimension[1] - 10),
                    1.0,
                    class_name == "allies" and (0, 255, 0, 255) or (0, 0, 255, 255),
                )

        self.__ndi_helper.send(image_editor.image)
