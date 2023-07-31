from overrides import final, override
from structures import OpenCVImage, ProducerBase
from time import sleep
from .dxshot import DXCamera, create, device_info, output_info


class ImageProducer(ProducerBase[OpenCVImage]):
    __camera: DXCamera

    def __init__(self):
        super().__init__(self.__class__.__name__)

    @final
    @override
    def _run_before_loop(self) -> None:
        print("Initializing DxCam...")
        print(device_info())
        print(output_info())
        self.__camera = create(output_color="BGR")
        sleep(1.0)
        print("DxCam initialized")
        self.__camera.start()

    @final
    @override
    def _produce(self) -> OpenCVImage:
        return self.__camera.get_latest_frame()

    @final
    @override
    def _run_after_loop(self) -> None:
        self.__camera.stop()
