from weapon_factory import WeaponSubscriber as __WeaponSubscriber


class RecoilSuppressor(__WeaponSubscriber):
    def __init__(self):
        super().__init__(self.__class__.__name__)
