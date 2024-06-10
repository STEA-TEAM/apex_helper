from dataclasses import dataclass
from json import dumps
from overrides import final
from typing import Any
from .ws_action import WsAction


@dataclass
class WsMessage:
    def __init__(self, ws_action: WsAction, data: Any = None):
        self.action = ws_action
        self.data = data

    @final
    def __str__(self) -> str:
        return dumps(self.__dict__)
