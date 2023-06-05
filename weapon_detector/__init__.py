from datetime import datetime
from pyautogui import size as get_screen_size
from typing import List

import cv2
import numpy as np

from screen_recorder import ImageHandler

from .constants import (
    AMMO_COLOR_DICT,
    LEFT_SOLT, RIGHT_SOLT,
    ORIGIN_SCREEN_SIZE,
    WEAPON_ICON_DICT,
    WEAPON_INFO_DICT,
)
from .types import Rectangle, AmmoInfo, AmmoType
from .utils import (
    get_point_color,
    image_in_polygon,
    image_in_rectangle,
    scale_point,
    scale_polygon,
    scale_rectangle,
)


class WeaponDetector(ImageHandler):
    __timestamps: List[float] = [datetime.now().timestamp()]
    __scale: float
    __weapon_area: Rectangle
    __weapon_left: AmmoInfo
    __weapon_right: AmmoInfo

    def __init__(self):
        screen_size = get_screen_size()
        print(f"Initializing with screen size: {screen_size}")
        self.__scale = screen_size[0] / ORIGIN_SCREEN_SIZE
        print(f"Scale: {self.__scale}")
        self.__weapon_area = (
            (screen_size[0] - round(832 * self.__scale), screen_size[1] - round(252 * self.__scale)),
            (screen_size[0] - round(101 * self.__scale), screen_size[1] - round(45 * self.__scale))
        )

    def __call__(self, image):
        cropped_image = image_in_rectangle(image, self.__weapon_area)
        ammo_info = self.__get_ammo_infos(cropped_image)
        weapon_identity = self.__get_weapon_identity(cropped_image, ammo_info)
        self.__display_info(cropped_image, ammo_info, weapon_identity)

    def __get_ammo_infos(self, img) -> AmmoInfo | None:
        weapon_left: AmmoInfo
        weapon_right: AmmoInfo

        weapon_left_color = get_point_color(img, scale_point(self.__scale, LEFT_SOLT))
        weapon_right_color = get_point_color(img, scale_point(self.__scale, RIGHT_SOLT))

        cv2.circle(img, scale_point(self.__scale, LEFT_SOLT), 3, (0, 0, 255, 40), 1)
        cv2.circle(img, scale_point(self.__scale, RIGHT_SOLT), 3, (0, 0, 255, 40), 1)

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

    def __get_weapon_identity(self, img, ammo_info: AmmoInfo | None) -> str | None:
        if ammo_info is None:
            return None
        weapon_info_list = WEAPON_INFO_DICT[ammo_info["type"]]
        if weapon_info_list.__len__() == 1:
            return weapon_info_list[0]["name"]
        weapon_icon_area = WEAPON_ICON_DICT[ammo_info["type"]]
        weapon_image = image_in_polygon(img, scale_polygon(self.__scale, weapon_icon_area))
        cv2.polylines(img, scale_polygon(self.__scale, weapon_icon_area), True, (0, 0, 255, 127), 1)
        for weapon_info in weapon_info_list:
            # TODO: Implement eigenvalues
            # eigenvalues = cv2.calcHist([weapon_image], [0], None, [256], [0, 256])
            # if weapon_info["eigenvalues"] == eigenvalues:
            return weapon_info["name"]
        return None

    def __display_info(self, img, ammo_info: AmmoInfo | None, weapon_identity: str | None):
        self.__timestamps.append(datetime.now().timestamp())
        if self.__timestamps.__len__() > 5:
            self.__timestamps.pop(0)

        ammo_info_text = f'Ammo type: {ammo_info["type"].value}' if ammo_info is not None else 'Ammo type: Unknown'
        weapon_identity_text = f'Weapon identity: {weapon_identity}'
        fps_text = f'Fps: {round(1 / np.average(np.diff(self.__timestamps)), 2)}'

        cv2.putText(img, ammo_info_text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(img, ammo_info_text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,), 1, cv2.LINE_AA)
        cv2.putText(img, weapon_identity_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(img, weapon_identity_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,), 1, cv2.LINE_AA)
        cv2.putText(img, fps_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(img, fps_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,), 1, cv2.LINE_AA)

        cv2.imshow("Weapon Area", cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC))
