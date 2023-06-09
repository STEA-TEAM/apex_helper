from cv2 import boundingRect
from numpy import ndarray as opencv_image, abs, int16, max, min, sum, uint8, where
from typing import LiteralString, Tuple

from .constants import AMMO_COLOR_DICT, LEFT_SOLT, RIGHT_SOLT, WEAPON_ICON_AREA
from .types import AmmoInfo, AmmoType, Point, Rectangle


def get_point_color(image: opencv_image, point: Point) -> int:
    pixel = image[point[1], point[0]]
    return (pixel[2] << 16) + (pixel[1] << 8) + pixel[0]


def image_in_rectangle(image: opencv_image, rectangle: Rectangle) -> opencv_image:
    return image[rectangle[0][1]:rectangle[1][1], rectangle[0][0]:rectangle[1][0]]


def image_relative_diff(image: opencv_image, ref_color, threshold) -> opencv_image:
    result = image.astype(int16)
    result_diff = abs(result - ref_color)
    result_sum = sum(where(result_diff > 0, result_diff, 0), axis=2)
    threshold_sum = (max(result_sum) - min(result_sum)) * threshold
    return where(result_sum > threshold_sum, 255, 0).astype(uint8)


def get_ammo_infos(image: opencv_image) -> AmmoInfo | None:
    weapon_left: AmmoInfo
    weapon_right: AmmoInfo

    weapon_left_color = get_point_color(image, LEFT_SOLT)
    weapon_right_color = get_point_color(image, RIGHT_SOLT)

    if weapon_left_color in AMMO_COLOR_DICT:
        weapon_left = AMMO_COLOR_DICT[weapon_left_color]
    else:
        weapon_left = {
            "type": AmmoType.Unknown,
            "active": False
        }

    if weapon_right_color in AMMO_COLOR_DICT:
        weapon_right = AMMO_COLOR_DICT[weapon_right_color]
    else:
        weapon_right = {
            "type": AmmoType.Unknown,
            "active": False
        }

    if weapon_left["active"]:
        return weapon_left
    elif weapon_right["active"]:
        return weapon_right
    else:
        return None


def get_weapon_eigenvalues(image: opencv_image, threshold: float = 0.95) -> Tuple[float, float, float, float]:
    weapon_image = image_in_rectangle(image, WEAPON_ICON_AREA)
    weapon_image = image_relative_diff(weapon_image, weapon_image[-1, 0], threshold)
    bounding_rectangle = boundingRect(weapon_image)

    return (
        round(bounding_rectangle[0] / weapon_image.shape[1] * 100, 4),
        round((bounding_rectangle[0] + bounding_rectangle[2]) / weapon_image.shape[1] * 100, 4),
        round(bounding_rectangle[1] / weapon_image.shape[0] * 100, 4),
        round((bounding_rectangle[1] + bounding_rectangle[3]) / weapon_image.shape[0] * 100, 4),
    )


def get_weapon_identity(image: opencv_image, ammo_info: AmmoInfo | None) -> LiteralString | None:
    from numpy import abs, array, inf, sum

    from .constants import WEAPON_INFO_DICT

    if ammo_info is None:
        return None
    weapon_info_list = WEAPON_INFO_DICT[ammo_info["type"]]
    if weapon_info_list.__len__() == 1:
        return weapon_info_list[0]["name"]

    eigenvalues = get_weapon_eigenvalues(image)

    current_weapon = {
        "sum": inf,
        "name": None
    }

    for weapon_info in weapon_info_list:
        eigenvalues_diff_sum = sum(abs(array(eigenvalues) - array(weapon_info["eigenvalues"])))
        if eigenvalues_diff_sum < current_weapon["sum"]:
            current_weapon["sum"] = eigenvalues_diff_sum
            current_weapon["name"] = weapon_info["name"]
    return current_weapon["name"]
