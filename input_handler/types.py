from enum import Enum
from pynput import keyboard, mouse
from typing import TypeAlias, TypedDict, Tuple


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
    key: keyboard.Key | keyboard.KeyCode


class KeyReleaseEvent(TypedDict):
    key: keyboard.Key | keyboard.KeyCode


InputEvent: TypeAlias = (
    MouseMoveEvent
    | MouseClickEvent
    | MouseScrollEvent
    | KeyPressEvent
    | KeyReleaseEvent
)
InputPayload: TypeAlias = Tuple[InputType, InputEvent]
