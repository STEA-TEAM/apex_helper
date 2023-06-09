from enum import Enum
from typing import LiteralString, Tuple, TypeAlias, TypedDict

Color = Tuple[int, int, int]
Point: TypeAlias = Tuple[int, int]
Rectangle: TypeAlias = Tuple[Tuple[int, int], Tuple[int, int]]
