from weapon_detector import WeaponProcessor as __WeaponProcessor


class RecoilSuppressor(__WeaponProcessor):
    def __init__(self):
        super().__init__(self.__class__.__name__)
