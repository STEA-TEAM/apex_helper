from enum import Enum
from typing import TypedDict, TypeAlias

Point: TypeAlias = tuple[int, int]
Rectangle: TypeAlias = tuple[tuple[int, int], tuple[int, int]]
Polygon: TypeAlias = list[tuple[int, int]]


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
    name: str
    eigenvalues: tuple[float, float, float, float]
