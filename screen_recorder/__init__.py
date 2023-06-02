from abc import ABC, abstractmethod
from threading import Thread, Event

import cv2
import numpy as np
import pyautogui


class ImageHandler(ABC):
    @abstractmethod
    def __call__(self, image):
        pass


class ScreenRecorder:
    __handler_map: dict[str, callable] = {}
    __stop_event: Event = Event()
    __thread_handle: Thread

    def __init__(self):
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

    def __capture_screen(self):
        while True:
            if self.__stop_event.is_set():
                self.__stop_event.clear()
                return

            image = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
            for handler in self.__handler_map.values():
                handler(image)
