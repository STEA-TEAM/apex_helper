from structures import CV2Image, Point, Rectangle
from utils import image_in_rectangle, image_relative_diff
from .constants import (
    AMMO_COLOR_DICT,
    ORIGIN_SCREEN_SIZE,
    WEAPON_AREA_BOUNDARIES,
    WEAPON_ICON_AREA,
    WEAPON_INFO_DICT,
)
from .types import AmmoType, EigenValues, WeaponIdentity

import cv2
import numpy as np


def get_point_color(image: CV2Image, point: Point) -> int:
    pixel = image[point[1], point[0]]
    return (pixel[2] << 16) + (pixel[1] << 8) + pixel[0]


def get_weapon_area(image_shape: Point) -> Rectangle:
    (width, height) = image_shape
    (left_top, right_bottom) = WEAPON_AREA_BOUNDARIES
    (left_top_x, left_top_y) = left_top
    (right_bottom_x, right_bottom_y) = right_bottom
    return (
        (width - left_top_x, height - left_top_y),
        (width - right_bottom_x, height - right_bottom_y),
    )


def get_weapon_eigen_values(
    image: CV2Image, threshold: float = 0.95
) -> (EigenValues, Rectangle):
    weapon_image = image_in_rectangle(image, WEAPON_ICON_AREA)
    weapon_image = image_relative_diff(weapon_image, weapon_image[-1, 0], threshold)
    bounding_rectangle = cv2.boundingRect(weapon_image)

    return (
        round(bounding_rectangle[0] / weapon_image.shape[1] * 100, 4),
        round(
            (bounding_rectangle[0] + bounding_rectangle[2])
            / weapon_image.shape[1]
            * 100,
            4,
        ),
        round(bounding_rectangle[1] / weapon_image.shape[0] * 100, 4),
        round(
            (bounding_rectangle[1] + bounding_rectangle[3])
            / weapon_image.shape[0]
            * 100,
            4,
        ),
    ), bounding_rectangle


def get_weapon_identity(
    eigen_values: EigenValues, ammo_type: AmmoType
) -> WeaponIdentity:
    if ammo_type == AmmoType.Unknown:
        return WeaponIdentity.Unknown
    weapon_info_list = WEAPON_INFO_DICT[ammo_type]
    if weapon_info_list.__len__() == 1:
        return weapon_info_list[0]["identity"]

    current_weapon = {"sum": np.inf, "name": None}

    for weapon_info in weapon_info_list:
        eigenvalues_diff_sum = np.sum(
            np.abs(np.array(eigen_values) - np.array(weapon_info["eigenvalues"]))
        )
        if eigenvalues_diff_sum < current_weapon["sum"]:
            current_weapon["sum"] = eigenvalues_diff_sum
            current_weapon["name"] = weapon_info["identity"]
    return current_weapon["name"]


def scale_screen(screen: Point) -> Point:
    (width, height) = screen
    scale = ORIGIN_SCREEN_SIZE / width
    return round(width * scale), round(height * scale)


def color_relative_diff(color: int, ref_color: int) -> int:
    return (
        abs((color >> 16 & 0xFF) - (ref_color >> 16 & 0xFF))
        + abs((color >> 8 & 0xFF) - (ref_color >> 8 & 0xFF))
        + abs((color & 0xFF) - (ref_color & 0xFF))
    )


def get_ammo_type(left_ammo_color: int, right_ammo_color: int) -> AmmoType:
    min_diff = 0xFFFFFF
    result = AmmoType.Unknown
    for ammo_type, ammo_color in AMMO_COLOR_DICT.items():
        diff = min(
            color_relative_diff(left_ammo_color, ammo_color),
            color_relative_diff(right_ammo_color, ammo_color),
        )
        if diff < min_diff:
            min_diff = diff
            result = ammo_type
    if min_diff > 0x4:
        return AmmoType.Unknown
    return result
