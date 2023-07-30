from numpy import ndarray as opencv_image
from overrides import override
from structures import ProducerBase
from time import sleep

from .dxshot import DXCamera, create, device_info, output_info


class ImageProducer(ProducerBase[opencv_image]):
    __camera: DXCamera

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
