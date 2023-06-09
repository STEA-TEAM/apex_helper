from enum import Enum
from typing import LiteralString, Tuple, TypeAlias, TypedDict

Point: TypeAlias = Tuple[int, int]
Rectangle: TypeAlias = Tuple[Tuple[int, int], Tuple[int, int]]


class AmmoType(Enum):
    Unknown = "Unknown"
    Heavy = "Heavy"
    Light = "Light"
    Energy = "Energy"
    Shotgun = "Shotgun"
    Sniper = "Sniper"
    Mythic = "Mythic"
    Sheila = "Sheila"
    Sentry = "Sentry"


class AmmoInfo(TypedDict):
    type: AmmoType
    active: bool


class WeaponInfo(TypedDict):
    name: LiteralString
    eigenvalues: Tuple[float, float, float, float]
