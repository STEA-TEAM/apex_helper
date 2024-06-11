from enum import EnumMeta
from typing import List, Optional, TypeAlias, TypedDict
from .ws_action import WsAction
from .ws_message import ServerResult, WsMessage


class DrawType(EnumMeta):
    Circle = "Circle"
    Line = "Line"
    Rectangle = "Rectangle"
    Text = "Text"


class Fill(TypedDict):
    color: str
    opacity: Optional[float]


class Stroke(TypedDict):
    color: str
    opacity: Optional[float]
    width: Optional[int]


class BaseElement(TypedDict):
    type: DrawType
    fill: Optional[Fill]
    opacity: Optional[float]
    stroke: Optional[Stroke]


class CircleDimensions(TypedDict):
    radius: float
    x: float
    y: float


class CircleElement(BaseElement):
    dimensions: CircleDimensions


class LineDimensions(TypedDict):
    x1: float
    x2: float
    y1: float
    y2: float


class LineElement(BaseElement):
    dimensions: LineDimensions


class RectangleDimensions(TypedDict):
    height: float
    width: float
    x: float
    y: float


class RectangleElement(BaseElement):
    dimensions: RectangleDimensions


class TextDimensions(TypedDict):
    x: float
    y: float


class TextFont(TypedDict):
    family: Optional[str]
    size: float


class TextElement(BaseElement):
    content: str
    dimensions: TextDimensions
    font: Optional[TextFont]


DrawElement: TypeAlias = CircleElement | LineElement | RectangleElement | TextElement


class Data(ServerResult):
    elements: List[DrawElement]
    name: str


class LayerDrawServerMessage(WsMessage):
    def __init__(self, data: Data):
        WsMessage.__init__(self, WsAction.LayerDraw, data)
