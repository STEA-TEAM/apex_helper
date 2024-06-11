from dataclasses import dataclass
from enum import EnumMeta
from json import dumps
from overrides import final
from typing import Any, Optional, TypedDict
from .ws_action import WsAction


class ResultType(EnumMeta):
    failure = "failure"
    error = "error"
    success = "success"


class ServerResult(TypedDict):
    result: ResultType
    message: Optional[str]


@dataclass
class WsMessage:
    def __init__(self, ws_action: WsAction, data: Any = None):
        self.action = ws_action
        self.data = data

    @final
    def __str__(self) -> str:
        return dumps(self.__dict__)
