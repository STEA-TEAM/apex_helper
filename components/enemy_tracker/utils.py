from components.device_adapters import DeviceType, MouseEventFlag, DeviceInstruction
from structures import Point

import numpy as np


def get_distance(point1: Point, point2: Point) -> float:
    return np.linalg.norm(np.array(point1) - np.array(point2)).astype(float)


def move_to(
        start_point: Point,
        end_point: Point,
        distance: float,
        control_signal: float,
        dt: float
) -> DeviceInstruction:
    direction = (np.array(end_point) - np.array(start_point)) / distance
    return (
        DeviceType.Mouse,
        (
            [MouseEventFlag.Move],
            (control_signal * direction * dt).astype(int).tolist(),
            0
        ),
        0
    )
