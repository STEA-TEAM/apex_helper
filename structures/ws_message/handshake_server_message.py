from typing import TypedDict
from .ws_action import WsAction
from .ws_message import WsMessage


class Resolution(TypedDict):
    height: int
    width: int


class Data(TypedDict):
    resolution: Resolution
    fps: int
    name: str


class HandshakeServerMessage(WsMessage):
    def __init__(self, data: Data):
        WsMessage.__init__(self, WsAction.Handshake, data)
