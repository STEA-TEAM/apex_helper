from datetime import datetime
from threading import Event, Thread

from constants import ORIGIN_SCREEN_SIZE, LEFT_SOLT, RIGHT_SOLT, AMMO_COLOR_DICT
from types import AmmoInfo
from utils import get_point_color

import cv2
import numpy as np
import pyautogui


class WeaponManager:
    __scale: float
    __weapon_area: (int, int, int, int)
    __weapon_left: AmmoInfo
    __weapon_right: AmmoInfo

    __thread_handle: Thread
    __stop_event: Event

    def __init__(self, config):
        screen_size = pyautogui.size()
        print(f"Initializing with screen size: {screen_size}")
        self.__scale = screen_size[0] / ORIGIN_SCREEN_SIZE
        area_width = round(731 * self.__scale)
        area_height = round(207 * self.__scale)
        self.__weapon_area[0] = screen_size[0] - area_width - round(101 * self.__scale)
        self.__weapon_area[1] = screen_size[1] - area_height - round(45 * self.__scale)
        self.__weapon_area[2] = area_width
        self.__weapon_area[3] = area_height
        print(f"Initialized weapon area: {self.__weapon_area}")
        self.__thread_handle = Thread(target=self.__weapon_detector)

    def start(self):
        if self.__thread_handle.is_alive():
            print("Weapon Manager is already running")
            return
        self.__thread_handle.start()

    def stop(self):
        self.__stop_event.set()

    def __weapon_detector(self):
        while True:
            if self.__stop_event.is_set():
                self.__stop_event.clear()
                return
            weapon_area_image = cv2.cvtColor(
                np.asarray(pyautogui.screenshot(region=self.__weapon_area)), cv2.COLOR_RGB2BGR
            )

            ammo_info = self.__get_ammo_infos(weapon_area_image)
            res = self.__get_weapon_identity(weapon_area_image, ammo_info)
            print("Result : ", datetime.now(), res)

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

    def __get_weapon_identity(self, img, ammo_info: AmmoInfo | None) -> int:
        if ammo_info is None:
            return None


        return 0
