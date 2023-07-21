from device_factory.types import MouseEventFlag


class MouseEmulator:
    from threading import Event as __Event, Thread as __Thread
    from typing import List as __List
    from .types import MouseEvent as __MouseEvent

    __events: __List[__MouseEvent] = []
    __stop_event: __Event = __Event()
    __thread_handle: __Thread

    def __init__(self):
        from threading import Thread

        self.__thread_handle = Thread(target=self.__process_mouse_events)

    def start(self) -> None:
        if self.__thread_handle.is_alive():
            print(f"{self.__class__.__name__} is already running")
            return
        print(f"Starting {self.__class__.__name__}...")
        self.__thread_handle.start()

    def stop(self) -> None:
        if not self.__thread_handle.is_alive():
            print(f"{self.__class__.__name__} is not running")
            return
        print(f"Stopping {self.__class__.__name__}...")
        self.__stop_event.set()
        self.__thread_handle.join()

    def push_events(self, events: __List[__MouseEvent]) -> None:
        self.__events += events

    def replace_events(self, events: __List[__MouseEvent], force: bool) -> None:
        self.__events = events if force else [self.__events[0]] + events

    def __process_mouse_events(self):
        from ctypes import windll
        from functools import reduce
        from time import sleep

        while True:
            while len(self.__events) > 0:
                if self.__stop_event.is_set():
                    break
                (event_flags, point, data, delay) = self.__events[0]
                windll.user32.mouse_event(reduce(lambda x, y: x | y, event_flags), point[0], point[1], data, 0)
                sleep(delay)
                self.__events.pop(0)
            if self.__stop_event.is_set():
                break
            sleep(0.01)
        self.__stop_event.clear()
