from abc import ABC as __ABC


class ImageConsumer(__ABC):
    from abc import abstractmethod as __abstractmethod
    from numpy import ndarray as __opencv_image
    from threading import Event as __Event, Lock as __Lock, Thread as __Thread
    from typing import LiteralString as __LiteralString

    __current_image: __opencv_image | None = None
    __image_lock: __Lock = __Lock()
    __stop_event: __Event = __Event()

    __name: __LiteralString
    __thread_handle: __Thread

    def __init__(self, name: __LiteralString):
        from threading import Thread

        self.__name = name
        self.__thread_handle = Thread(target=self.__run)
        return

    def name(self) -> __LiteralString:
        return self.__name

    def start(self) -> None:
        if self.__thread_handle.is_alive():
            print(f"{self.__name} is already running")
            return
        print(f"Starting {self.__name}...")
        self.__thread_handle.start()

    def stop(self) -> None:
        if not self.__thread_handle.is_alive():
            print(f"{self.__name} is not running")
            return
        print(f"Stopping {self.__name}...")
        self.__stop_event.set()
        self.__thread_handle.join()

    def feed(self, image: __opencv_image) -> None:
        if not self.__image_lock.locked():
            self.__current_image = image

    @__abstractmethod
    def process_image(self, image: __opencv_image) -> None:
        pass

    def __run(self) -> None:
        from time import sleep as __sleep

        while True:
            if self.__stop_event.is_set():
                break
            if self.__current_image is not None:
                self.process_image(self.__get_image())
            else:
                __sleep(0.001)
        self.__stop_event.clear()

    def __get_image(self) -> __opencv_image:
        self.__image_lock.acquire()
        image = self.__current_image.copy()
        self.__image_lock.release()
        return image


class ImageProducer:
    from threading import Event as __Event, Thread as __Thread
    from typing import Dict as __Dict, LiteralString as __LiteralString

    from .dxshot import DXCamera as __DXCamera

    __camera: __DXCamera
    __consumer_map: __Dict[__LiteralString, ImageConsumer] = {}
    __stop_event: __Event = __Event()
    __thread_handle: __Thread

    def __init__(self):
        from time import sleep
        from threading import Thread

        from .dxshot import create

        print("Initializing DxCam...")
        self.__camera = create(output_idx=0, output_color="BGR")
        self.__thread_handle = Thread(target=self.__capture_screen)
        sleep(1.0)
        print("DxCam initialized")

    def register(self, consumer: ImageConsumer) -> None:
        self.__consumer_map[consumer.name()] = consumer

    def unregister(self, name: __LiteralString) -> None:
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
        self.__camera.start()
        while True:
            if self.__stop_event.is_set():
                break
            image = self.__camera.get_latest_frame()
            for consumer in self.__consumer_map.values():
                consumer.feed(image)
        self.__stop_event.clear()
        self.__camera.stop()
