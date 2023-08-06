from overrides import final, override
from structures import OpenCVImage, TaskerManagerBase, ReusableThread
from time import sleep
from .dxshot import DXCamera, create, device_info, output_info


class ImageProducer(TaskerManagerBase[OpenCVImage], ReusableThread):
    @final
    @override
    def _thread_loop(self) -> None:
        image = self.__camera.get_latest_frame()
        self._start_tasks(image)

    def __init__(self):
        self.__camera: DXCamera = create(output_color="BGR")

        TaskerManagerBase.__init__(self)
        ReusableThread.__init__(self)
        print("Initialized DxCam...")
        print(device_info())
        print(output_info())

    @final
    @override
    def _run_before_loop(self) -> None:
        sleep(1.0)
        self.__camera.start()

    @final
    @override
    def _run_after_loop(self) -> None:
        self.__camera.stop()
