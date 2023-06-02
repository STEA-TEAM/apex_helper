from datetime import datetime

import cv2
import numpy as np
from pyautogui import size as get_screen_size

from screen_recorder import ImageHandler
from weapon_detector.constants import *
from weapon_detector.types import RectArea, AmmoInfo, AmmoType
from weapon_detector.utils import get_image_part, get_point_color, get_scaled_point, get_scaled_rect_area


class WeaponDetector(ImageHandler):
    __timestamps: List[float] = [datetime.now().timestamp()]
    __scale: float
    __weapon_area: RectArea
    __weapon_left: AmmoInfo
    __weapon_right: AmmoInfo

    def __init__(self):
        screen_size = get_screen_size()
        print(f"Initializing with screen size: {screen_size}")
        self.__scale = screen_size[0] / ORIGIN_SCREEN_SIZE
        self.__weapon_area = {
            "x1": screen_size[0] - round(832 * self.__scale),
            "y1": screen_size[1] - round(252 * self.__scale),
            "x2": screen_size[0] - round(101 * self.__scale),
            "y2": screen_size[1] - round(45 * self.__scale),
        }

        print(f"Initialized weapon area: {self.__weapon_area}")

    def __call__(self, image):
        cropped_image = get_image_part(image, self.__weapon_area)
        ammo_info = self.__get_ammo_infos(cropped_image)
        weapon_identity = self.__get_weapon_identity(cropped_image, ammo_info)
        self.__display_info(cropped_image, ammo_info, weapon_identity)

    def __get_ammo_infos(self, img) -> AmmoInfo | None:
        weapon_left: AmmoInfo
        weapon_right: AmmoInfo

        weapon_left_color = get_point_color(img, get_scaled_point(self.__scale, LEFT_SOLT))
        weapon_right_color = get_point_color(img, get_scaled_point(self.__scale, RIGHT_SOLT))
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
        for weapon_info in weapon_info_list:
            weapon_image = get_image_part(img, get_scaled_rect_area(self.__scale, WEAPON_ICON_AREA))
            # TODO: Implement eigenvalues
            # eigenvalues = cv2.calcHist([weapon_image], [0], None, [256], [0, 256])
            # if weapon_info["eigenvalues"] == eigenvalues:
            return weapon_info["name"]
        return None

    def __display_info(self, img, ammo_info: AmmoInfo | None, weapon_identity: str | None):
        self.__timestamps.append(datetime.now().timestamp())
        if self.__timestamps.__len__() > 5:
            self.__timestamps.pop(0)
        if ammo_info is not None:
            ammo_info_text = f'{ammo_info["type"].value}'
        else:
            ammo_info_text = 'Unknown'
        th, img = cv2.threshold(img, 254, 255, cv2.THRESH_BINARY)
        cv2.putText(img, f'Ammo type: {ammo_info_text}',
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(img, f'Weapon identity: {weapon_identity}',
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(img, f'Fps: {round(1 / np.average(np.diff(self.__timestamps)), 2)}',
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.imshow("Weapon Area", img)
