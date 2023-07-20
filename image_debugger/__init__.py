class ImageDebugger:
    from datetime import datetime as __datetime
    from numpy import ndarray as __opencv_image
    from typing import List as __List, LiteralString as __LiteralString
    from .types import Color as __Color, Point as __Point, Rectangle as __Rectangle

    __image: __opencv_image | None = None
    __window_name: __LiteralString
    __custom_scale: float
    __timestamps: __List[float] = [__datetime.now().timestamp()]

    def __init__(self, window_name: __LiteralString = "Image Debugger", custom_scale: float = 1.0):
        self.__window_name = window_name
        self.__custom_scale = custom_scale

    def set_image(self, image: __opencv_image):
        self.__image = image.copy()

    def add_circle(self, center: __Point, radius: int, color: __Color = (0, 0, 255), thickness: int = 1):
        from cv2 import circle

        if self.__image is not None:
            circle(self.__image, center, radius, color, thickness)

    def add_rectangle(self, rectangle: __Rectangle, color: __Color = (0, 0, 255), thickness: int = 1):
        from cv2 import rectangle

        if self.__image is not None:
            rectangle(self.__image, rectangle[0], rectangle[1], color, thickness)

    def add_texts(
            self,
            texts: __List[__LiteralString],
            size: float = 0.5,
            color: __Color = (0, 0, 0),
            thickness: int = 1
    ):
        from cv2 import copyMakeBorder, putText, BORDER_CONSTANT, FONT_HERSHEY_SIMPLEX, LINE_AA

        if self.__image is not None:
            old_height = self.__image.shape[0]
            self.__image = copyMakeBorder(
                self.__image,
                0,
                (texts.__len__()) * 20,
                0,
                0,
                BORDER_CONSTANT,
                None,
                value=(255, 255, 255)
            )
            for index, text in enumerate(texts):
                putText(
                    self.__image,
                    text,
                    (5, 15 + old_height + index * 20),
                    FONT_HERSHEY_SIMPLEX,
                    size,
                    color,
                    thickness,
                    LINE_AA
                )

    def show(self):
        from cv2 import imshow, putText, resize, waitKey, FONT_HERSHEY_SIMPLEX, INTER_LINEAR, LINE_AA
        from datetime import datetime
        from numpy import average, diff, round

        self.__timestamps.append(datetime.now().timestamp())
        if self.__timestamps.__len__() > 5:
            self.__timestamps.pop(0)

        if self.__image is not None:
            fps_text = f'Fps: {round(1 / average(diff(self.__timestamps)), 2)}'
            image = self.__image.copy()
            putText(image, fps_text, (5, 15), FONT_HERSHEY_SIMPLEX, 0.5, (127, 127, 127), 5, LINE_AA)
            putText(image, fps_text, (5, 15), FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, LINE_AA)
            imshow(
                self.__window_name,
                resize(
                    image,
                    None,
                    fx=self.__custom_scale,
                    fy=self.__custom_scale,
                    interpolation=INTER_LINEAR
                )
            )
            waitKey(1)
