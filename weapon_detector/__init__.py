import screen_recorder


class WeaponDetector(screen_recorder.ImageHandler):
    from typing import List
    from datetime import datetime
    from pyautogui import size as get_screen_size
    from .types import Rectangle, AmmoInfo

    __window_name: str
    __custom_ratio: float
    __timestamps: List[float] = [datetime.now().timestamp()]
    __scaled_shape: (int, int)
    __weapon_area: Rectangle
    __weapon_left: AmmoInfo
    __weapon_right: AmmoInfo

    def __init__(
            self,
            window_name: str,
            custom_ratio: float = 1.0,
            screen_size: tuple[int, int] = get_screen_size(),
    ):
        from numpy import round, divide

        from .constants import ORIGIN_SCREEN_SIZE

        self.__window_name = window_name
        self.__custom_ratio = custom_ratio
        print(f"Initializing with screen size: {screen_size}")
        self.__scaled_shape = round(divide(screen_size, screen_size[0] / ORIGIN_SCREEN_SIZE)).astype(int)
        self.__weapon_area = (
            (self.__scaled_shape[0] - 832, self.__scaled_shape[1] - 252),
            (self.__scaled_shape[0] - 101, self.__scaled_shape[1] - 45)
        )

    def __call__(self, image):
        from cv2 import resize, INTER_NEAREST
        from .utils import image_in_rectangle, get_ammo_infos, get_weapon_identity

        cropped_image = image_in_rectangle(resize(
            image,
            self.__scaled_shape,
            interpolation=INTER_NEAREST
        ), self.__weapon_area)
        ammo_info = get_ammo_infos(cropped_image)
        weapon_identity = get_weapon_identity(cropped_image, ammo_info)
        if self.__window_name is not None:
            self.__display_info(cropped_image, ammo_info, weapon_identity)

    def __display_info(self, img, ammo_info: AmmoInfo | None, weapon_identity: str | None):
        from cv2 import (
            boundingRect,
            circle,
            imshow,
            putText,
            rectangle,
            resize,
            FONT_HERSHEY_SIMPLEX,
            INTER_LINEAR,
            LINE_AA
        )
        from datetime import datetime
        from numpy import average, diff, round, uint8, zeros

        from .constants import LEFT_SOLT, RIGHT_SOLT, WEAPON_ICON_AREA
        from .utils import image_in_rectangle, image_relative_diff, get_weapon_eigenvalues

        self.__timestamps.append(datetime.now().timestamp())
        if self.__timestamps.__len__() > 5:
            self.__timestamps.pop(0)

        weapon_image = image_in_rectangle(img, WEAPON_ICON_AREA)
        weapon_image = image_relative_diff(weapon_image, weapon_image[-1, 0], 0.75)

        bounding_rectangle = boundingRect(weapon_image)

        eigenvalues = get_weapon_eigenvalues(img)

        rectangle(
            img,
            (WEAPON_ICON_AREA[0][0] + bounding_rectangle[0], WEAPON_ICON_AREA[0][1] + bounding_rectangle[1]),
            (WEAPON_ICON_AREA[0][0] + bounding_rectangle[0] + bounding_rectangle[2],
             WEAPON_ICON_AREA[0][1] + bounding_rectangle[1] + bounding_rectangle[3]),
            (255, 255, 0, 127), 1
        )
        circle(img, LEFT_SOLT, 3, (0, 0, 255, 40), 1)
        circle(img, RIGHT_SOLT, 3, (0, 0, 255, 40), 1)
        rectangle(img, WEAPON_ICON_AREA[0], WEAPON_ICON_AREA[1], (0, 0, 255, 127), 1)

        extended_image = zeros((img.shape[0] + 100, img.shape[1], 3), uint8)
        extended_image[:, :] = (255, 255, 255)
        extended_image[:img.shape[0], :img.shape[1]] = img.copy()

        fps_text = f'        Fps: {round(1 / average(diff(self.__timestamps)), 2)}'
        ammo_info_text = f'     Ammo: {ammo_info["type"].value if ammo_info is not None else "Unknown"}'
        weapon_identity_text = f'    Weapon: {weapon_identity}'
        eigenvalues_text = f'Eigenvalues: {eigenvalues}'

        putText(extended_image, fps_text, (10, img.shape[0] + 20), FONT_HERSHEY_SIMPLEX, 0.5, (0,), 1,
                LINE_AA)
        putText(extended_image, ammo_info_text, (10, img.shape[0] + 40), FONT_HERSHEY_SIMPLEX, 0.5, (0,), 1,
                LINE_AA)
        putText(extended_image, weapon_identity_text, (10, img.shape[0] + 60), FONT_HERSHEY_SIMPLEX, 0.5, (0,), 1,
                LINE_AA)
        putText(extended_image, eigenvalues_text, (10, img.shape[0] + 80), FONT_HERSHEY_SIMPLEX, 0.5, (0,), 1,
                LINE_AA)

        imshow(
            self.__window_name,
            resize(
                extended_image,
                None,
                fx=self.__custom_ratio,
                fy=self.__custom_ratio,
                interpolation=INTER_LINEAR
            )
        )
