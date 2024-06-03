import torch
import math

from cv2 import resize
from numpy import floor
from overrides import override, final
from typing import AnyStr
from ultralytics import YOLO

from image_debugger import ImageDebugger
from structures import TaskerBase, PublisherBase
from structures import OpenCVImage
from weapon_detector.utils import image_in_rectangle


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


class PlayerDetector(TaskerBase[OpenCVImage], PublisherBase):
    def __init__(self, model_path: AnyStr, model_image_size: int = 640):
        self.__debugger: ImageDebugger | None = None
        self.__is_aborted: bool = False
        self.__model_image_size: int = model_image_size
        self.__model = YOLO(model_path).to(get_torch_device())
        TaskerBase.__init__(self)
        PublisherBase.__init__(self)
        print(f"Initialized with model image size: {model_image_size}")

    @final
    def set_debugger(self, debugger: ImageDebugger) -> None:
        self.__debugger = debugger

    @final
    @override
    def _abort_task(self) -> None:
        self.__is_aborted = True

    @final
    @override
    def _start_task(self, payload: OpenCVImage) -> None:
        self.__is_aborted = False

        cropped_image = image_in_rectangle(
            payload,
            (
                (math.floor(payload.shape[1] / 2 - payload.shape[0] / 2), 0),
                (
                    math.floor(payload.shape[1] / 2 + payload.shape[0] / 2),
                    payload.shape[0],
                ),
            ),
        )

        if self.__debugger is not None:
            self.__debugger.set_image(
                resize(
                    cropped_image,
                    (
                        math.floor(cropped_image.shape[1] / 2),
                        math.floor(cropped_image.shape[0] / 2),
                    ),
                )
            )

        if self.__is_aborted:
            return

        results = self.__model.predict(source=cropped_image, verbose=False)
        for result in results:
            for box in result.boxes:
                dimensions = floor(box.xyxy[0].cpu().numpy() / 2).astype(int)
                if self.__debugger is not None:
                    self.__debugger.add_rectangle(
                        ((dimensions[0], dimensions[1]), (dimensions[2], dimensions[3]))
                    )
            # masks = result.masks  # Masks object for segmentation masks outputs
            # keypoints = result.keypoints  # Keypoints object for pose outputs
            # probs = result.probs  # Probs object for classification outputs
            # obb = result.obb  # Oriented boxes object for OBB outputs
            # result.show()  # display to screen
            # result.save(filename="result.jpg")  # save to disk

        if self.__debugger is not None:
            self.__debugger.show()
