from overrides import override
from structures import ReusableThread
from time import sleep
from typing import Dict, LiteralString

from .dxshot import DXCamera, create, device_info, output_info
from .image_consumer import ImageConsumer


class ImageProducer(ReusableThread):
    __camera: DXCamera
    __consumer_map: Dict[LiteralString, ImageConsumer] = {}

    @override
    def start(self) -> None:
        super().start()
        for consumer in self.__consumer_map.values():
            consumer.start()

    @override
    def stop(self) -> None:
        super().stop()
        for consumer in self.__consumer_map.values():
            consumer.stop()

    def register(self, consumer: ImageConsumer) -> None:
        self.__consumer_map[consumer.name()] = consumer

    def unregister(self, name: LiteralString) -> None:
        del self.__consumer_map[name]

    @override
    def _run_before_loop(self) -> None:
        print("Initializing DxCam...")
        print(device_info())
        print(output_info())
        self.__camera = create(output_color="BGR")
        sleep(1.0)
        print("DxCam initialized")
        self.__camera.start()

    @override
    def _thread_loop(self) -> None:
        image = self.__camera.get_latest_frame()
        for consumer in self.__consumer_map.values():
            consumer.feed(image)

    @override
    def _run_after_loop(self) -> None:
        self.__camera.stop()

