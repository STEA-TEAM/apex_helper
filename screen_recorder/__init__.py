import abc


class ImageHandler(abc.ABC):
    @abc.abstractmethod
    def __call__(self, image):
        pass


class ScreenRecorder:
    from dxcam import DXCamera
    from threading import Event, Thread

    __camera: DXCamera
    __handler_map: dict[str, callable] = {}
    __stop_event: Event = Event()
    __thread_handle: Thread

    def __init__(self):
        from dxcam import create
        from time import sleep
        from threading import Thread

        print("Initializing DxCam...")
        self.__camera = create(output_idx=0, output_color="BGR")
        self.__thread_handle = Thread(target=self.__capture_screen)
        sleep(1.0)
        print("DxCam initialized")

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
        from cv2 import destroyAllWindows

        if not self.__thread_handle.is_alive():
            print("Screen Recorder is not running")
            return
        print("Stopping Screen Recorder")
        self.__stop_event.set()
        self.__thread_handle.join()
        destroyAllWindows()

    def __capture_screen(self):
        from cv2 import waitKey

        self.__camera.start()

        while True:
            image = self.__camera.get_latest_frame()
            if image is not None:
                for handler in self.__handler_map.values():
                    handler(image)
            if self.__stop_event.is_set():
                break
            waitKey(1)

        self.__stop_event.clear()
        self.__camera.stop()
