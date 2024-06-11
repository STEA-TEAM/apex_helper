from enum import EnumMeta


class WsAction(EnumMeta):
    Handshake = "Handshake"
    LayerClear = "LayerClear"
    LayerDraw = "LayerDraw"
