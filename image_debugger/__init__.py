class ImageDebugger:
    from numpy import ndarray as opencv_image
    from typing import List, LiteralString

    from .types import Color, Point, Rectangle

    __image: opencv_image | None
    __window_name: LiteralString | None

    def __init__(self, window_name: LiteralString = "Image Debugger", custom_scale: float = 1.0):
        self.__window_name = window_name

    def set_image(self, image: opencv_image):
        self.__image = image.copy()

    def add_circle(self, center: Point, radius: int, color: Color = (0, 0, 255), thickness: int = 1):
        import cv2

        if self.__image is not None:
            cv2.circle(self.__image, center, radius, color, thickness)

    def add_rectangle(self, rectangle: Rectangle, color: Color = (0, 0, 255), thickness: int = 1):
        import cv2

        if self.__image is not None:
            cv2.rectangle(self.__image, rectangle[0], rectangle[1], color, thickness)

    def add_texts(self, texts: List[LiteralString], size: float = 0.5, color: Color = (0, 0, 0), thickness: int = 1):
        import cv2

        if self.__image is not None:
            cv2.copyMakeBorder(self.__image, 0, (texts.__len__() + 1) * 20, 0, 0, cv2.BORDER_CONSTANT, None, value=255)
            for index, text in enumerate(texts):
                cv2.putText(
                    self.__image,
                    text,
                    (10, self.__image.shape[0] + index * 20),
                    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    size,
                    color,
                    thickness
                )

    def show(self):
        import cv2

        if self.__image is not None:
            cv2.imshow(
                self.__window_name,
                cv2.resize(
                    self.__image,
                    None,
                    fx=custom_scale,
                    fy=custom_scale,
                    interpolation=cv2.INTER_LINEAR
                )
            )
            cv2.waitKey(1)
