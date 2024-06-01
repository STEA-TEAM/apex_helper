from enum import Enum, IntFlag
from pynput import keyboard
from typing import List, AnyStr, Tuple, TypeAlias


class DeviceType(Enum):
    Idle = "Idle"
    Mouse = "Mouse"
    Keyboard = "Keyboard"


class MouseEventFlag(IntFlag):
    Move = 0x0001
    LeftDown = 0x0002
    LeftUp = 0x0004
    RightDown = 0x0008
    RightUp = 0x0010
    MiddleDown = 0x0020
    MiddleUp = 0x0040
    SideDown = 0x0080
    SideUp = 0x0100
    WheelScroll = 0x0800
    WheelTilt = 0x01000
    AbsolutePosition = 0x8000


class MouseSideButton(IntFlag):
    Front = 0x0001
    Back = 0x0002


Point: TypeAlias = Tuple[int, int]
MouseEvent: TypeAlias = Tuple[List[MouseEventFlag], Point, MouseSideButton | int]
KeyboardEvent: TypeAlias = List[Tuple[keyboard.Key | AnyStr, bool]]
DeviceEvent: TypeAlias = MouseEvent | KeyboardEvent
DeviceInstruction: TypeAlias = Tuple[DeviceType, DeviceEvent | None, float]
