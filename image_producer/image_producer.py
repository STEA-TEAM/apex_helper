from overrides import final, override
from structures import OpenCVImage, TaskerManagerBase, ReusableThread
from time import sleep
from .dxshot import DXCamera, create, device_info, output_info


class ImageProducer(TaskerManagerBase[OpenCVImage], ReusableThread):
    __camera: DXCamera

    @final
    @override
    def _thread_loop(self) -> None:
        image = self.__camera.get_latest_frame()
        self._start_tasks(image)

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
        print(self._tasker_map)

    @final
    @override
    def _run_after_loop(self) -> None:
        self.__camera.stop()
