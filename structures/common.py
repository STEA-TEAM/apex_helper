from numpy import ndarray
from typing import Tuple, TypeAlias

RGB: TypeAlias = Tuple[int, int, int]
RGBA: TypeAlias = Tuple[int, int, int, int]
CV2Image: TypeAlias = ndarray
Point: TypeAlias = Tuple[int, int]
Rectangle: TypeAlias = Tuple[Point, Point]
