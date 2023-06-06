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
    WEAPON_ICON_AREA,
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

        weapon_icon_area = scale_rectangle(self.__scale, WEAPON_ICON_AREA)
        weapon_image = image_in_rectangle(img, weapon_icon_area)
        bounding_rectangle = cv2.boundingRect(cv2.inRange(weapon_image, (255, 255, 255), (255, 255, 255)))

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

        weapon_icon_area = scale_rectangle(self.__scale, WEAPON_ICON_AREA)
        weapon_image = cv2.inRange(image_in_rectangle(img, weapon_icon_area), (255, 255, 255), (255, 255, 255))
        bounding_rectangle = cv2.boundingRect(weapon_image)
        eigenvalues = (
            round(bounding_rectangle[2] / weapon_image.shape[1] * 100, 4),
            round(bounding_rectangle[3] / weapon_image.shape[0] * 100, 4),
            round(np.sum(weapon_image) / 2.55 / (weapon_image.shape[1] * weapon_image.shape[0]), 4)
        )

        # img = cv2.inRange(img, (255, 255, 255), (255, 255, 255))
        # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        cv2.rectangle(
            img,
            (weapon_icon_area[0][0] + bounding_rectangle[0], weapon_icon_area[0][1] + bounding_rectangle[1]),
            (weapon_icon_area[0][0] + bounding_rectangle[0] + bounding_rectangle[2],
             weapon_icon_area[0][1] + bounding_rectangle[1] + bounding_rectangle[3]),
            (255, 255, 0, 127), 1
        )
        cv2.circle(img, scale_point(self.__scale, LEFT_SOLT), 3, (0, 0, 255, 40), 1)
        cv2.circle(img, scale_point(self.__scale, RIGHT_SOLT), 3, (0, 0, 255, 40), 1)
        weapon_icon_area = scale_rectangle(self.__scale, WEAPON_ICON_AREA)
        cv2.rectangle(img, weapon_icon_area[0], weapon_icon_area[1], (0, 0, 255, 127), 1)

        scaled_image = np.zeros((img.shape[0] + 100, img.shape[1], 3), np.uint8)
        scaled_image[:, :] = (255, 255, 255)
        scaled_image[:img.shape[0], :img.shape[1]] = img.copy()

        fps_text = f'Fps: {round(1 / np.average(np.diff(self.__timestamps)), 2)}'
        ammo_info_text = f'Ammo type: {ammo_info["type"].value}' if ammo_info is not None else 'Ammo type: Unknown'
        weapon_identity_text = f'Weapon identity: {weapon_identity}'
        eigenvalues_text = f'Eigenvalues: {eigenvalues}'

        cv2.putText(scaled_image, fps_text, (10, img.shape[0] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,), 1,
                    cv2.LINE_AA)
        cv2.putText(scaled_image, ammo_info_text, (10, img.shape[0] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,), 1,
                    cv2.LINE_AA)
        cv2.putText(scaled_image, weapon_identity_text, (10, img.shape[0] + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,), 1,
                    cv2.LINE_AA)
        cv2.putText(scaled_image, eigenvalues_text, (10, img.shape[0] + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,), 1,
                    cv2.LINE_AA)

        cv2.imshow("Weapon Area Mask", cv2.resize(scaled_image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC))
