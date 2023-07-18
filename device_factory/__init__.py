class MouseEmulator:
    from threading import Event as __Event, Thread as __Thread
    from typing import List
    from .types import MouseEvent as __MouseEvent

    __stop_event: __Event = __Event()
    __thread_handle: __Thread
    __event_queue: List[__MouseEvent]

    def __init__(self):
        from threading import Thread

        self.__thread_handle = Thread(target=self.__process_mouse_events)

    def __process_mouse_events(self):
        from ctypes import windll
        from functools import reduce
        from time import sleep

        while True:
            while len(self.__event_queue) > 0:
                if self.__stop_event.is_set():
                    break
                (event_flags, point, data, delay) = self.__event_queue[0]
                windll.user32.mouse_event(reduce(lambda x, y: x | y, event_flags), point[0], point[1], data, 0)
                sleep(delay)
            if self.__stop_event.is_set():
                break
            sleep(0.01)
        self.__stop_event.clear()
