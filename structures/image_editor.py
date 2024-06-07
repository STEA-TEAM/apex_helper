import cv2

from enum import Enum
from numpy import ndarray
from structures import CV2Image, Point, Rectangle, RGB
from typing import Any, AnyStr, List, Tuple


class EditType(Enum):
    CIRCLE = 1
    RECTANGLE = 3
    TEXT = 4


class ImageEditor:
    def __init__(self, image: ndarray):
        self.__image: ndarray = image
        self.edit_history: List[Tuple[EditType, List[Any]]] = []

    def add_circle(
        self, center: Point, radius: int, color: RGB = (0, 0, 255), thickness: int = 1
    ):
        self.edit_history.append((EditType.CIRCLE, [center, radius, color, thickness]))

    def add_rectangle(
        self, rectangle: Rectangle, color: RGB = (0, 0, 255), thickness: int = 1
    ):
        self.edit_history.append((EditType.RECTANGLE, [rectangle, color, thickness]))

    def add_text(
        self,
        text: AnyStr,
        position: Point,
        size: float = 0.5,
        color: RGB = (0, 0, 255),
        thickness: int = 1,
    ):
        self.edit_history.append(
            (EditType.TEXT, [text, position, size, color, thickness])
        )

    @property
    def image(self) -> CV2Image:
        for edit_type, params in self.edit_history:
            if edit_type == EditType.CIRCLE:
                center, radius, color, thickness = params
                cv2.circle(self.__image, center, radius, color, thickness)
            elif edit_type == EditType.RECTANGLE:
                rectangle, color, thickness = params
                cv2.rectangle(
                    self.__image, rectangle[0], rectangle[1], color, thickness
                )
            elif edit_type == EditType.TEXT:
                text, position, size, color, thickness = params
                cv2.putText(
                    self.__image,
                    text,
                    position,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    size,
                    color,
                    thickness,
                    cv2.LINE_AA,
                )
        return self.__image

    @property
    def original_image(self) -> CV2Image:
        return self.__image
