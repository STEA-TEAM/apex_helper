class WeaponSubscriber:
    from typing import LiteralString as __LiteralString
    from .types import AmmoInfo as __AmmoInfo

    _current_ammo: __AmmoInfo | None = None
    _current_weapon: str | None = None
    __name: __LiteralString

    def __init__(self, name: __LiteralString):
        self.__name = name
        return

    def name(self) -> __LiteralString:
        return self.__name

    def notify(self, ammo: __AmmoInfo, weapon: str) -> None:
        self._current_ammo = ammo
        self._current_weapon = weapon
