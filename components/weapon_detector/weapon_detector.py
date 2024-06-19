from cv2 import INTER_NEAREST_EXACT, resize
from overrides import override, final
from pyautogui import size as get_screen_size

from structures import TaskerBase, PublisherBase, ImageEditor
from structures import CV2Image, Point, Rectangle
from structures import NdiHelper
from .constants import (
    LEFT_SOLT,
    RIGHT_SOLT,
    WEAPON_ICON_AREA,
)
from .types import WeaponIdentity
from .utils import (
    get_ammo_type,
    get_point_color,
    get_weapon_area,
    get_weapon_eigen_values,
    get_weapon_identity,
    image_in_rectangle,
    scale_screen,
)

import numpy as np


class WeaponDetector(TaskerBase[CV2Image], PublisherBase[WeaponIdentity]):
    def __init__(self, screen_size: Point = get_screen_size()):
        self.__is_aborted: bool = False
        self.__ndi_helper: NdiHelper = NdiHelper("WeaponDetector")
        self.__scaled_shape: Point = scale_screen(screen_size)
        self.__weapon_area: Rectangle = get_weapon_area(self.__scaled_shape)

        TaskerBase.__init__(self)
        PublisherBase.__init__(self)

        print(f"WeaponDetector initialized with screen size: {screen_size}")

    @final
    @override
    def _abort_task(self) -> None:
        self.__is_aborted = True

    @final
    @override
    def _start_task(self, payload: CV2Image) -> None:
        self.__is_aborted = False

        offset: Point = self.__weapon_area[0]
        cropped_image = image_in_rectangle(
            resize(payload, self.__scaled_shape, interpolation=INTER_NEAREST_EXACT),
            self.__weapon_area,
        )
        if self.__is_aborted:
            return

        image_editor = ImageEditor(
            np.zeros((payload.shape[0], payload.shape[1], 4), dtype=np.uint8)
        )
        image_editor.add_circle((offset[0] + LEFT_SOLT[0], offset[1] + LEFT_SOLT[1]), 3)
        image_editor.add_circle(
            (offset[0] + RIGHT_SOLT[0], offset[1] + RIGHT_SOLT[1]), 3
        )
        image_editor.add_rectangle(self.__weapon_area, (255, 255, 255, 127))
        image_editor.add_rectangle(
            (
                (
                    offset[0] + WEAPON_ICON_AREA[0][0],
                    offset[1] + WEAPON_ICON_AREA[0][1],
                ),
                (
                    offset[0] + WEAPON_ICON_AREA[1][0],
                    offset[1] + WEAPON_ICON_AREA[1][1],
                ),
            )
        )
        if self.__is_aborted:
            return

        ammo_type = get_ammo_type(
            get_point_color(cropped_image, LEFT_SOLT),
            get_point_color(cropped_image, RIGHT_SOLT),
        )
        image_editor.add_text(f"Ammo: {ammo_type.value}", (offset[0], offset[1] - 75))
        if self.__is_aborted:
            return

        eigen_values, bounding_rectangle = get_weapon_eigen_values(cropped_image)
        image_editor.add_rectangle(
            (
                (
                    offset[0] + WEAPON_ICON_AREA[0][0] + bounding_rectangle[0],
                    offset[1] + WEAPON_ICON_AREA[0][1] + bounding_rectangle[1],
                ),
                (
                    offset[0]
                    + WEAPON_ICON_AREA[0][0]
                    + bounding_rectangle[0]
                    + bounding_rectangle[2],
                    offset[1]
                    + WEAPON_ICON_AREA[0][1]
                    + bounding_rectangle[1]
                    + bounding_rectangle[3],
                ),
            ),
            (255, 255, 0, 255),
        )
        image_editor.add_text(
            f"Eigen values: {eigen_values}", (offset[0], offset[1] - 45)
        )
        if self.__is_aborted:
            return

        weapon_identity = get_weapon_identity(eigen_values, ammo_type)
        image_editor.add_text(f"Weapon: {weapon_identity}", (offset[0], offset[1] - 15))
        if self.__is_aborted:
            return

        self.__ndi_helper.send(image_editor.image)
        self._publish(weapon_identity)
