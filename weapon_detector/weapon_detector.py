from typing import Tuple

import numpy as np
from cv2 import INTER_AREA, INTER_CUBIC, INTER_NEAREST_EXACT, boundingRect, resize
from overrides import override, final
from pyautogui import size as get_screen_size

from image_debugger import ImageDebugger
from structures import TaskerBase, PublisherBase
from structures import OpenCVImage, Point, Rectangle
from .constants import (
    AMMO_COLOR_DICT,
    LEFT_SOLT,
    RIGHT_SOLT,
    WEAPON_ICON_AREA,
    WEAPON_INFO_DICT,
)
from .types import AmmoInfo, AmmoType, WeaponIdentity
from .utils import (
    image_in_rectangle,
    image_relative_diff,
    get_point_color,
    get_weapon_area,
    scale_screen,
)


class WeaponDetector(TaskerBase[OpenCVImage], PublisherBase):
    def __init__(self, screen_size: Point = get_screen_size()):
        self.__debugger: ImageDebugger | None = None
        self.__is_aborted: bool = False
        self.__scaled_shape: Point = scale_screen(screen_size)
        self.__weapon_area: Rectangle = get_weapon_area(self.__scaled_shape)

        TaskerBase.__init__(self)
        PublisherBase.__init__(self)
        print(f"Initialized with screen size: {screen_size}")

    @final
    def set_debugger(self, debugger: ImageDebugger) -> None:
        self.__debugger = debugger

    @final
    @override
    def _abort_task(self) -> None:
        self.__is_aborted = True

    @final
    @override
    def _start_task(self, payload: OpenCVImage) -> None:
        self.__is_aborted = False

        cropped_image = image_in_rectangle(
            resize(payload, self.__scaled_shape, interpolation=INTER_NEAREST_EXACT),
            self.__weapon_area,
        )

        if self.__is_aborted:
            return

        if self.__debugger is not None:
            self.__debugger.set_image(
                image_in_rectangle(
                    resize(
                        payload,
                        self.__scaled_shape,
                        interpolation=INTER_AREA
                        if self.__scaled_shape[0] < payload.shape[1]
                        else INTER_CUBIC,
                    ),
                    self.__weapon_area,
                )
            )

        ammo_info = self.__get_ammo_infos(cropped_image)
        if self.__is_aborted:
            return

        weapon_identity = self.__get_weapon_identity(cropped_image, ammo_info)
        if self.__is_aborted:
            return

        if self.__debugger is not None:
            ammo_info_text = f'     Ammo: {ammo_info["type"].value if ammo_info is not None else "Unknown"}'
            weapon_identity_text = f"    Weapon: {weapon_identity}"
            self.__debugger.add_texts([ammo_info_text, weapon_identity_text])
            self.__debugger.show()

        self._publish(weapon_identity)

    @final
    def __get_ammo_infos(self, image: OpenCVImage) -> AmmoInfo | None:
        weapon_left: AmmoInfo
        weapon_right: AmmoInfo

        weapon_left_color = get_point_color(image, LEFT_SOLT)
        weapon_right_color = get_point_color(image, RIGHT_SOLT)

        if self.__debugger is not None:
            self.__debugger.add_circle(LEFT_SOLT, 3)
            self.__debugger.add_circle(RIGHT_SOLT, 3)

        if weapon_left_color in AMMO_COLOR_DICT:
            weapon_left = AMMO_COLOR_DICT[weapon_left_color]
        else:
            weapon_left = {"type": AmmoType.Unknown, "active": False}

        if weapon_right_color in AMMO_COLOR_DICT:
            weapon_right = AMMO_COLOR_DICT[weapon_right_color]
        else:
            weapon_right = {"type": AmmoType.Unknown, "active": False}

        if weapon_left["active"]:
            return weapon_left
        elif weapon_right["active"]:
            return weapon_right
        else:
            return None

    @final
    def __get_weapon_identity(
            self, image: OpenCVImage, ammo_info: AmmoInfo | None
    ) -> WeaponIdentity:
        if ammo_info is None:
            return WeaponIdentity.Unknown
        weapon_info_list = WEAPON_INFO_DICT[ammo_info["type"]]
        if weapon_info_list.__len__() == 1:
            return weapon_info_list[0]["identity"]

        eigenvalues = self.__get_weapon_eigenvalues(image)

        if self.__debugger is not None:
            eigenvalues_text = f"Eigenvalues: {eigenvalues}"
            self.__debugger.add_texts([eigenvalues_text])

        current_weapon = {"sum": np.inf, "name": None}

        for weapon_info in weapon_info_list:
            eigenvalues_diff_sum = np.sum(
                np.abs(np.array(eigenvalues) - np.array(weapon_info["eigenvalues"]))
            )
            if eigenvalues_diff_sum < current_weapon["sum"]:
                current_weapon["sum"] = eigenvalues_diff_sum
                current_weapon["name"] = weapon_info["identity"]
        return current_weapon["name"]

    @final
    def __get_weapon_eigenvalues(
            self, image: OpenCVImage, threshold: float = 0.95
    ) -> Tuple[float, float, float, float]:
        weapon_image = image_in_rectangle(image, WEAPON_ICON_AREA)
        weapon_image = image_relative_diff(weapon_image, weapon_image[-1, 0], threshold)
        bounding_rectangle = boundingRect(weapon_image)

        if self.__debugger is not None:
            self.__debugger.add_rectangle(WEAPON_ICON_AREA)
            self.__debugger.add_rectangle(
                (
                    (
                        WEAPON_ICON_AREA[0][0] + bounding_rectangle[0],
                        WEAPON_ICON_AREA[0][1] + bounding_rectangle[1],
                    ),
                    (
                        WEAPON_ICON_AREA[0][0]
                        + bounding_rectangle[0]
                        + bounding_rectangle[2],
                        WEAPON_ICON_AREA[0][1]
                        + bounding_rectangle[1]
                        + bounding_rectangle[3],
                    ),
                ),
                (255, 255, 0),
            )

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
        )
