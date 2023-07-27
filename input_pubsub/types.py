from enum import Enum
from typing import TypeAlias, TypedDict

from pynput import mouse
from pynput.keyboard import Key, KeyCode


class InputType(Enum):
    MouseMove = "MouseMove"
    MouseClick = "MouseClick"
    MouseScroll = "MouseScroll"
    KeyPress = "KeyPress"
    KeyRelease = "KeyRelease"


class MouseMoveEvent(TypedDict):
    x: int
    y: int


class MouseClickEvent(TypedDict):
    x: int
    y: int
    button: mouse.Button
    pressed: bool


class MouseScrollEvent(TypedDict):
    x: int
    y: int
    dx: int
    dy: int


class KeyPressEvent(TypedDict):
    key: Key | KeyCode


class KeyReleaseEvent(TypedDict):
    key: Key | KeyCode


InputEvent: TypeAlias = MouseMoveEvent | MouseClickEvent | MouseScrollEvent | KeyPressEvent | KeyReleaseEvent
