from numpy import ndarray
from typing import Tuple, TypeAlias

Color: TypeAlias = Tuple[int, int, int]
OpenCVImage: TypeAlias = ndarray
Point: TypeAlias = Tuple[int, int]
Rectangle: TypeAlias = Tuple[Point, Point]
