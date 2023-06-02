from datetime import datetime

import cv2
from pyautogui import size as get_screen_size

from screen_recorder import ImageHandler
from weapon_detector.constants import ORIGIN_SCREEN_SIZE, LEFT_SOLT, RIGHT_SOLT, AMMO_COLOR_DICT
from weapon_detector.types import RectArea, AmmoInfo, AmmoType
from weapon_detector.utils import get_image_part, get_point_color


class WeaponDetector(ImageHandler):
    __last_time: datetime = datetime.now()
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
        current_time = datetime.now()
        cv2.putText(cropped_image, f'Ammo info: {ammo_info}',
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(cropped_image, f'Weapon identity: {weapon_identity}',
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(cropped_image, f'Fps: {round(10 ** 6 / (current_time - self.__last_time).microseconds, 2)}',
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        self.__last_time = current_time
        cv2.imshow("Weapon Area", cropped_image)

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

        return ""
