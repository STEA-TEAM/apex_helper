import time
from abc import ABC, abstractmethod
from threading import Thread, Event

import cv2
import dxcam


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
        self.__camera = dxcam.create()
        time.sleep(0.1)
        self.__thread_handle = Thread(target=self.__capture_screen)

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
        self.__stop_event.set()
        self.__thread_handle.join()
        cv2.destroyAllWindows()

    def __capture_screen(self):
        self.__camera.start()
        time.sleep(0.1)

        while True:
            image = self.__camera.get_latest_frame()
            if image is not None:
                # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                cv2.imshow("Screen Recorder", image)
                # for handler in self.__handler_map.values():
                #     handler(image)
            if cv2.waitKey(1) & 0xFF == ord("q") or self.__stop_event.is_set():
                break

        self.__stop_event.clear()
        time.sleep(0.1)
        self.__camera.stop()
