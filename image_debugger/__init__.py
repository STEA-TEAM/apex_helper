class ImageDebugger:
    from datetime import datetime
    from numpy import ndarray as opencv_image
    from typing import List, LiteralString

    from .types import Color, Point, Rectangle

    __image: opencv_image | None = None
    __window_name: LiteralString
    __custom_scale: float
    __timestamps: List[float] = [datetime.now().timestamp()]

    def __init__(self, window_name: LiteralString = "Image Debugger", custom_scale: float = 1.0):
        self.__window_name = window_name
        self.__custom_scale = custom_scale

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
            old_height = self.__image.shape[0]
            self.__image = cv2.copyMakeBorder(
                self.__image,
                0,
                (texts.__len__() + 1) * 20,
                0,
                0,
                cv2.BORDER_CONSTANT,
                None,
                value=(255, 255, 255)
            )
            for index, text in enumerate(texts):
                cv2.putText(
                    self.__image,
                    text,
                    (10, old_height + (index + 1) * 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    size,
                    color,
                    thickness
                )

    def show(self):
        import cv2
        from datetime import datetime
        from numpy import average, diff, round

        self.__timestamps.append(datetime.now().timestamp())
        if self.__timestamps.__len__() > 5:
            self.__timestamps.pop(0)

        if self.__image is not None:
            fps_text = f'Fps: {round(1 / average(diff(self.__timestamps)), 2)}'
            image = self.__image.copy()
            image = cv2.putText(image, fps_text, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (127, 127, 127), 2)
            image = cv2.putText(image, fps_text, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            cv2.imshow(
                self.__window_name,
                cv2.resize(
                    image,
                    None,
                    fx=self.__custom_scale,
                    fy=self.__custom_scale,
                    interpolation=cv2.INTER_LINEAR
                )
            )
            cv2.waitKey(1)
