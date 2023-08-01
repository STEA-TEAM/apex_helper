from enum import Enum
from typing import Tuple, TypedDict


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


class WeaponIdentity(Enum):
    Alternator = "Alternator SMG"
    Bocek = "Bocek Compound Bow"
    Car = "C.A.R. SMG"
    ChargeRifle = "Charge Rifle"
    Devotion = "Devotion LMG"
    Eva8 = "EVA-8 Auto"
    Flatline = "VK-47 Flatline"
    G7 = "G7 Scout"
    Havoc = "HAVOC Rifle"
    Hemlok = "Hemlok Burst AR"
    Knife = "Throwing Knife"
    Kraber = "Kraber .50-Cal Sniper"
    Longbow = "Longbow DMR"
    LStar = "L-STAR EMG"
    Mastiff = "Mastiff Shotgun"
    Mozambique = "Mozambique Shotgun"
    Nemesis = "Nemesis Burst AR"
    P2020 = "P2020"
    Peacekeeper = "Peacekeeper"
    Prowler = "Prowler Burst PDW"
    R301 = "R-301 Carbine"
    R3030 = "30-30 Repeater"
    R99 = "R-99 SMG"
    Rampage = "Rampage LMG"
    Re45 = "RE-45 Auto"
    Sentinel = "Sentinel"
    Sentry = "A-13 Sentry"
    Sheila = "Sheila"
    Spitfire = "M600 Spitfire"
    Triple = "Triple Take"
    Unknown = "Unknown"
    Volt = "Volt SMG"
    Wingman = "Wingman"


class WeaponInfo(TypedDict):
    eigenvalues: Tuple[float, float, float, float]
    identity: WeaponIdentity
