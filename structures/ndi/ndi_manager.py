from typing import AnyStr, Dict
from .ndi_helper import NdiHelper

import NDIlib


class NdiManager:
    def __init__(self):
        if not NDIlib.initialize():
            raise Exception("Failed to initialize NDIlib")

        self.__instances: Dict[AnyStr, NdiHelper] = {}

    def __del__(self):
        NDIlib.destroy()

    def get_channel(self, channel_name) -> NdiHelper:
        if channel_name not in self.__instances:
            self.__instances[channel_name] = NdiHelper(channel_name)
        return self.__instances[channel_name]

    def remove_channel(self, channel_name):
        self.__instances.pop(channel_name, None)


ndi_manager = NdiManager()
