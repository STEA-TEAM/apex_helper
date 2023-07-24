from .dxshot import DXCamera, create, device_info, output_info
from .image_consumer import ImageConsumer

from threading import Event, Thread
from time import sleep
from typing import Dict, LiteralString


class ImageProducer:
    __camera: DXCamera
    __consumer_map: Dict[LiteralString, ImageConsumer] = {}
    __stop_event: Event = Event()
    __thread_handle: Thread

    def __init__(self):
        print("Initializing DxCam...")
        print(device_info())
        print(output_info())
        self.__camera = create(output_color="BGR")
        self.__thread_handle = Thread(target=self.__capture_screen)
        sleep(1.0)
        print("DxCam initialized")

    def register(self, consumer: ImageConsumer) -> None:
        self.__consumer_map[consumer.name()] = consumer

    def unregister(self, name: LiteralString) -> None:
        del self.__consumer_map[name]

    def start(self) -> None:
        if self.__thread_handle.is_alive():
            print("Screen Recorder is already running")
            return
        for consumer in self.__consumer_map.values():
            consumer.start()
        self.__thread_handle.start()

    def stop(self) -> None:
        if not self.__thread_handle.is_alive():
            print("Screen Recorder is not running")
            return

        print("Stopping Producer...")
        self.__stop_event.set()
        self.__thread_handle.join()
        print("Stopping Consumers...")
        for consumer in self.__consumer_map.values():
            consumer.stop()

    def __capture_screen(self) -> None:
        import cv2
        self.__camera.start()
        while True:
            if self.__stop_event.is_set():
                break
            image = self.__camera.get_latest_frame()
            for consumer in self.__consumer_map.values():
                consumer.feed(image)
        self.__stop_event.clear()
        self.__camera.stop()
