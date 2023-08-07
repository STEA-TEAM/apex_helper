from typing import Tuple, TypeAlias

from numpy import ndarray

RGB: TypeAlias = Tuple[int, int, int]
RGBA: TypeAlias = Tuple[int, int, int, int]
OpenCVImage: TypeAlias = ndarray
Point: TypeAlias = Tuple[int, int]
Rectangle: TypeAlias = Tuple[Point, Point]
