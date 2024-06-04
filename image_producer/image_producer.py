from bettercam import BetterCam, create, device_info, output_info
from overrides import final, override
from structures import OpenCVImage, TaskerManagerBase, ReusableThread
from time import sleep


class ImageProducer(TaskerManagerBase[OpenCVImage], ReusableThread):
    @final
    @override
    def _thread_loop(self) -> None:
        image = self.__camera.get_latest_frame()
        self._start_tasks(image)

    def __init__(self):
        print("Initializing BetterCam...")
        print(device_info())
        print(output_info())

        self.__camera: BetterCam = create(output_color="BGR")

        TaskerManagerBase.__init__(self)
        ReusableThread.__init__(self)

    @final
    @override
    def _run_before_loop(self) -> None:
        self.__camera.start(target_fps=120)

    @final
    @override
    def _run_after_loop(self) -> None:
        self.__camera.stop()
