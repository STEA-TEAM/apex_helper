from datetime import datetime

import cv2

from structures import CV2Image, ImageEditor
from typing import AnyStr, List

import math
import NDIlib
import numpy as np


class NdiHelper:
    def __init__(self, ndi_name: AnyStr, max_fps: float = 60.0):
        setting = NDIlib.SendCreate()
        setting.ndi_name = ndi_name
        self.__ndi_send = NDIlib.send_create(setting)
        self.__timestamps: List[float] = [datetime.now().timestamp()]
        self.__video_frame = NDIlib.VideoFrameV2(
            FourCC=NDIlib.FOURCC_VIDEO_TYPE_BGRA,
            frame_rate_D=1000,
            frame_rate_N=math.floor(1000 * max_fps),
        )

    def __del__(self):
        NDIlib.send_destroy(self.__ndi_send)

    def send(self, image: CV2Image) -> None:
        fps_text = f"Fps: {self.__calculate_fps()}"
        image_editor = ImageEditor(image)
        image_editor.add_text(fps_text, (5, 15), 0.5, (127, 127, 127), 5)
        image_editor.add_text(fps_text, (5, 15), 0.5, (255, 255, 0), 1)
        data = cv2.cvtColor(image_editor.image, cv2.COLOR_BGR2BGRA)
        self.__video_frame.data = data
        NDIlib.send_send_video_async_v2(self.__ndi_send, self.__video_frame)

    def __calculate_fps(self) -> float:
        self.__timestamps.append(datetime.now().timestamp())
        if self.__timestamps.__len__() > 5:
            self.__timestamps.pop(0)
        return 1 / np.average(np.diff(self.__timestamps))
