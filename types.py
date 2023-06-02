from enum import Enum
from typing import TypedDict


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


class WeaponArea(TypedDict):
    x1: int
    y1: int
    x2: int
    y2: int


class WeaponInfo(TypedDict):
    name: str
    eigenvalues: tuple[float, float, float]
