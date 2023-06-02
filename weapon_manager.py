from datetime import datetime
from threading import Event, Thread

from constants import ORIGIN_SCREEN_SIZE, LEFT_SOLT, RIGHT_SOLT, AMMO_COLOR_DICT
from screen_recorder import ImageHandler
from types import AmmoInfo, WeaponArea
from utils import get_point_color

import cv2
import numpy as np
import pyautogui


class WeaponManager(ImageHandler):
    __scale: float
    __weapon_area: WeaponArea
    __weapon_left: AmmoInfo
    __weapon_right: AmmoInfo

    def __init__(self):
        screen_size = pyautogui.size()
        print(f"Initializing with screen size: {screen_size}")
        self.__scale = screen_size[0] / ORIGIN_SCREEN_SIZE
        self.__weapon_area["x2"] = screen_size[0] - round(101 * self.__scale)
        self.__weapon_area["y2"] = screen_size[1] - round(45 * self.__scale)
        self.__weapon_area["x1"] = self.__weapon_area["y2"] - round(731 * self.__scale)
        self.__weapon_area["y1"] = self.__weapon_area["y2"] - round(207 * self.__scale)

        print(f"Initialized weapon area: {self.__weapon_area}")

    def __call__(self, image):
        cropped_image = image[
                        self.__weapon_area["y1"]:self.__weapon_area["y2"],
                        self.__weapon_area["x1"]:self.__weapon_area["x2"]
                        ]
        ammo_info = self.__get_ammo_infos(cropped_image)
        weapon_identity = self.__get_weapon_identity(cropped_image, ammo_info)
        print("Ammo info: ", datetime.now(), ammo_info)
        print("Weapon identity: ", datetime.now(), weapon_identity)

    def __get_scaled_point(self, point: (int, int)) -> (int, int):
        return round(point[0] * self.__scale), round(point[1] * self.__scale)

    def __get_ammo_infos(self, img) -> AmmoInfo | None:
        weapon_left: AmmoInfo
        weapon_right: AmmoInfo

        weapon_left_color = get_point_color(img, self.__get_scaled_point(LEFT_SOLT))
        weapon_right_color = get_point_color(img, self.__get_scaled_point(RIGHT_SOLT))
        if weapon_left_color in AMMO_COLOR_DICT:
            weapon_left = AMMO_COLOR_DICT[weapon_left_color]
        else:
            weapon_left = {
                "type": "none",
                "active": False
            }
            print("No Weapon in Left Solt")

        if weapon_right_color in AMMO_COLOR_DICT:
            weapon_right = AMMO_COLOR_DICT[weapon_right_color]
        else:
            weapon_right = {
                "type": "none",
                "active": False
            }
            print("No Weapon in Right Solt")

        if weapon_left["active"]:
            return weapon_left
        elif weapon_right["active"]:
            return weapon_right
        else:
            return None

    def __get_weapon_identity(self, img, ammo_info: AmmoInfo | None) -> str | None:
        if ammo_info is None:
            return None

        return ""
