from components.device_adapters import DeviceType, MouseEventFlag, DeviceInstruction
from structures import Point

import numpy as np


def move_to(start_point: Point, end_point: Point) -> DeviceInstruction:
    offset = np.array(end_point) - np.array(start_point)
    direction = np.sign(offset)
    return (
        DeviceType.Mouse,
        (
            [MouseEventFlag.Move],
            np.multiply(np.multiply(np.log10(np.abs(offset) + 1), direction), 10).astype(int).tolist(),
            0
        ),
        0
    )
