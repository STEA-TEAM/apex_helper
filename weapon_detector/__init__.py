import screen_recorder


class WeaponDetector(screen_recorder.ImageHandler):
    from image_debugger import ImageDebugger
    from numpy import ndarray as opencv_image
    from pyautogui import size as get_screen_size
    from typing import LiteralString, Tuple
    from .types import AmmoInfo, Point, Rectangle

    __debugger: ImageDebugger | None = None
    __scaled_shape: (int, int)
    __weapon_area: Rectangle
    __weapon_left: AmmoInfo
    __weapon_right: AmmoInfo

    def __init__(
            self,
            screen_size: Point = get_screen_size(),
    ):
        from numpy import round, divide

        from .constants import ORIGIN_SCREEN_SIZE

        print(f"Initializing with screen size: {screen_size}")
        self.__scaled_shape = round(divide(screen_size, screen_size[0] / ORIGIN_SCREEN_SIZE)).astype(int)
        self.__weapon_area = (
            (self.__scaled_shape[0] - 832, self.__scaled_shape[1] - 252),
            (self.__scaled_shape[0] - 101, self.__scaled_shape[1] - 45)
        )

    def __call__(self, image: opencv_image):
        from cv2 import resize, INTER_NEAREST
        from .utils import image_in_rectangle

        cropped_image = image_in_rectangle(resize(
            image,
            self.__scaled_shape,
            interpolation=INTER_NEAREST
        ), self.__weapon_area)

        if self.__debugger is not None:
            self.__debugger.set_image(cropped_image)

        ammo_info = self.get_ammo_infos(cropped_image)
        weapon_identity = self.get_weapon_identity(cropped_image, ammo_info)
        if self.__debugger is not None:
            ammo_info_text = f'     Ammo: {ammo_info["type"].value if ammo_info is not None else "Unknown"}'
            weapon_identity_text = f'    Weapon: {weapon_identity}'
            self.__debugger.add_texts([ammo_info_text, weapon_identity_text])
            self.__debugger.show()

    def set_debugger(self, debugger: ImageDebugger):
        self.__debugger = debugger

    def get_ammo_infos(self, image: opencv_image) -> AmmoInfo | None:
        from .constants import AMMO_COLOR_DICT, LEFT_SOLT, RIGHT_SOLT
        from .types import AmmoInfo, AmmoType
        from .utils import get_point_color

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

    def get_weapon_eigenvalues(self, image: opencv_image, threshold: float = 0.95) -> Tuple[float, float, float, float]:
        from cv2 import boundingRect

        from .constants import WEAPON_ICON_AREA
        from .utils import image_in_rectangle, image_relative_diff

        weapon_image = image_in_rectangle(image, WEAPON_ICON_AREA)
        weapon_image = image_relative_diff(weapon_image, weapon_image[-1, 0], threshold)
        bounding_rectangle = boundingRect(weapon_image)

        if self.__debugger is not None:
            self.__debugger.add_rectangle(WEAPON_ICON_AREA)
            self.__debugger.add_rectangle(
                (
                    (
                        WEAPON_ICON_AREA[0][0] + bounding_rectangle[0],
                        WEAPON_ICON_AREA[0][1] + bounding_rectangle[1]
                    ),
                    (
                        WEAPON_ICON_AREA[0][0] + bounding_rectangle[0] + bounding_rectangle[2],
                        WEAPON_ICON_AREA[0][1] + bounding_rectangle[1] + bounding_rectangle[3]
                    )
                ),
                (255, 255, 0)
            )

        return (
            round(bounding_rectangle[0] / weapon_image.shape[1] * 100, 4),
            round((bounding_rectangle[0] + bounding_rectangle[2]) / weapon_image.shape[1] * 100, 4),
            round(bounding_rectangle[1] / weapon_image.shape[0] * 100, 4),
            round((bounding_rectangle[1] + bounding_rectangle[3]) / weapon_image.shape[0] * 100, 4),
        )

    def get_weapon_identity(self, image: opencv_image, ammo_info: AmmoInfo | None) -> LiteralString | None:
        from numpy import abs, array, inf, sum

        from .constants import WEAPON_INFO_DICT

        if ammo_info is None:
            return None
        weapon_info_list = WEAPON_INFO_DICT[ammo_info["type"]]
        if weapon_info_list.__len__() == 1:
            return weapon_info_list[0]["name"]

        eigenvalues = self.get_weapon_eigenvalues(image)

        if self.__debugger is not None:
            eigenvalues_text = f'Eigenvalues: {eigenvalues}'
            self.__debugger.add_texts([eigenvalues_text])

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
