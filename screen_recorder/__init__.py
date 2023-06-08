import time
from abc import ABC, abstractmethod
from threading import Thread, Event

import dxcam
import cv2


class ImageHandler(ABC):
    @abstractmethod
    def __call__(self, image):
        pass


class ScreenRecorder:
    __camera: dxcam.DXCamera
    __handler_map: dict[str, callable] = {}
    __stop_event: Event = Event()
    __thread_handle: Thread

    def __init__(self):
        print("Initializing DxCam...")
        self.__camera = dxcam.create(output_idx=0, output_color="BGR")
        self.__thread_handle = Thread(target=self.__capture_screen)
        time.sleep(1.0)
        print("DxCam initialized")

    def register(self, name, handler: ImageHandler):
        self.__handler_map[name] = handler

    def unregister(self, name):
        del self.__handler_map[name]

    def start(self):
        if self.__thread_handle.is_alive():
            print("Screen Recorder is already running")
            return
        self.__thread_handle.start()

    def stop(self):
        if not self.__thread_handle.is_alive():
            print("Screen Recorder is not running")
            return
        print("Stopping Screen Recorder")
        self.__stop_event.set()
        self.__thread_handle.join()
        cv2.destroyAllWindows()

    def __capture_screen(self):
        self.__camera.start()

        while True:
            image = self.__camera.get_latest_frame()
            if image is not None:
                for handler in self.__handler_map.values():
                    handler(image)
            if self.__stop_event.is_set():
                break
            cv2.waitKey(1)

        self.__stop_event.clear()
        self.__camera.stop()
