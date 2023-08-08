from structures import Point, Rectangle
from typing import Dict, List

from .types import AmmoType, AmmoInfo, WeaponInfo, WeaponIdentity

ORIGIN_SCREEN_SIZE = 3840
WEAPON_AREA_BOUNDARIES: Rectangle = ((832, 252), (101, 45))
WEAPON_ICON_AREA: Rectangle = ((74, 4), (400, 88))
LEFT_SOLT: Point = (40, 170)
RIGHT_SOLT: Point = (640, 170)

AMMO_COLOR_DICT: Dict[int, AmmoInfo] = {
    0x386B59: {
        "type": AmmoType.Heavy,
        "active": True
    },
    0x21342d: {
        "type": AmmoType.Heavy,
        "active": False
    },
    0x7d542d: {
        "type": AmmoType.Light,
        "active": True
    },
    0x3c2a1c: {
        "type": AmmoType.Light,
        "active": False
    },
    0x596e28: {
        "type": AmmoType.Energy,
        "active": True
    },
    0x2e361d: {
        "type": AmmoType.Energy,
        "active": False
    },
    0x6b2007: {
        "type": AmmoType.Shotgun,
        "active": True
    },
    0x30110a: {
        "type": AmmoType.Shotgun,
        "active": False
    },
    0x4b3f8f: {
        "type": AmmoType.Sniper,
        "active": True
    },
    0x241f43: {
        "type": AmmoType.Sniper,
        "active": False
    },
    0xb20136: {
        "type": AmmoType.Mythic,
        "active": True
    },
    0x54121f: {
        "type": AmmoType.Mythic,
        "active": False
    },
    0xa13ca1: {
        "type": AmmoType.Sheila,
        "active": True
    },
    0x3c6eb2: {
        "type": AmmoType.Sentry,
        "active": True
    },
}

WEAPON_INFO_DICT: Dict[AmmoType, List[WeaponInfo]] = {
    AmmoType.Energy: [
        {
            "eigenvalues": (11.4679, 100.0, 17.8571, 100.0),
            "identity": WeaponIdentity.Devotion,
        },
        {
            "eigenvalues": (15.5963, 94.0367, 12.5, 100.0),
            "identity": WeaponIdentity.Havoc,
        },
        {
            "eigenvalues": (21.5596, 92.2018, 12.5, 100.0),
            "identity": WeaponIdentity.LStar,
        },
        {
            "eigenvalues": (11.0092, 98.1651, 19.6429, 100.0),
            "identity": WeaponIdentity.Nemesis,
        },
        {
            "eigenvalues": (6.8807, 100.0, 7.1429, 100.0),
            "identity": WeaponIdentity.Triple,
        },
        {
            "eigenvalues": (23.8532, 87.6147, 25.0, 100.0),
            "identity": WeaponIdentity.Volt,
        },
    ],
    AmmoType.Heavy: [
        {
            "eigenvalues": (6.8807, 100.0, 23.2143, 94.6429),
            "identity": WeaponIdentity.R3030,
        },
        {
            "eigenvalues": (19.2661, 93.578, 10.7143, 98.2143),
            "identity": WeaponIdentity.Car,
        },
        {
            "eigenvalues": (15.5963, 91.7431, 12.5, 100.0),
            "identity": WeaponIdentity.Flatline,
        },
        {
            "eigenvalues": (19.7248, 92.6606, 7.1429, 100.0),
            "identity": WeaponIdentity.Hemlok,
        },
        {
            "eigenvalues": (36.2385, 84.4037, 12.5, 100.0),
            "identity": WeaponIdentity.Prowler,
        },
        {
            "eigenvalues": (8.7156, 100.0, 23.2143, 100.0),
            "identity": WeaponIdentity.Rampage,
        },

    ],
    AmmoType.Light: [
        {
            "eigenvalues": (39.9083, 78.4404, 14.2857, 100.0),
            "identity": WeaponIdentity.Alternator,
        },
        {
            "eigenvalues": (19.2661, 93.578, 10.7143, 98.2143),
            "identity": WeaponIdentity.Car,
        },
        {
            "eigenvalues": (11.9266, 100.0, 14.2857, 98.2143),
            "identity": WeaponIdentity.G7,
        },
        {
            "eigenvalues": (37.6147, 74.7706, 21.4286, 100.0),
            "identity": WeaponIdentity.P2020,
        },
        {
            "eigenvalues": (20.1835, 94.9541, 16.0714, 100.0),
            "identity": WeaponIdentity.R301,
        },
        {
            "eigenvalues": (25.2294, 96.3303, 10.7143, 100.0),
            "identity": WeaponIdentity.R99,
        },
        {
            "eigenvalues": (38.0734, 77.9817, 10.7143, 100.0),
            "identity": WeaponIdentity.Re45,
        },
        {
            "eigenvalues": (13.7615, 99.0826, 7.1429, 100.0),
            "identity": WeaponIdentity.Spitfire,
        },
    ],
    AmmoType.Mythic: [
        {
            "eigenvalues": (11.4679, 97.2477, 10.7143, 98.2143),
            "identity": WeaponIdentity.Bocek,
        },
        {
            "eigenvalues": (19.7248, 92.6606, 7.1429, 100.0),
            "identity": WeaponIdentity.Hemlok,
        },
        {
            "eigenvalues": (20.6422, 92.2018, 28.5714, 80.3571),
            "identity": WeaponIdentity.Knife,
        },
        {
            "eigenvalues": (2.2936, 100.0, 16.0714, 98.2143),
            "identity": WeaponIdentity.Kraber,
        },
        {
            "eigenvalues": (21.5596, 92.2018, 12.5, 100.0),
            "identity": WeaponIdentity.LStar,
        }
    ],
    AmmoType.Sentry: [
        {
            "eigenvalues": (4.1284, 100.0, 14.2857, 98.2143),
            "identity": WeaponIdentity.Sentry,
        }
    ],
    AmmoType.Sheila: [
        {
            "eigenvalues": (3.211, 95.8716, 7.1429, 100.0),
            "identity": WeaponIdentity.Sheila,
        }
    ],
    AmmoType.Shotgun: [
        {
            "eigenvalues": (17.8899, 99.5413, 12.5, 100.0),
            "identity": WeaponIdentity.Eva8,
        },
        {
            "eigenvalues": (5.0459, 100.0, 19.6429, 100.0),
            "identity": WeaponIdentity.Mastiff,
        },
        {
            "eigenvalues": (32.1101, 79.8165, 17.8571, 100.0),
            "identity": WeaponIdentity.Mozambique,
        },
        {
            "eigenvalues": (14.6789, 100.0, 14.2857, 92.8571),
            "identity": WeaponIdentity.Peacekeeper,
        },
    ],
    AmmoType.Sniper: [
        {
            "eigenvalues": (17.8899, 94.0367, 8.9286, 100.0),
            "identity": WeaponIdentity.ChargeRifle,
        },
        {
            "eigenvalues": (7.7982, 100.0, 19.6429, 91.0714),
            "identity": WeaponIdentity.Longbow,
        },
        {
            "eigenvalues": (3.211, 100.0, 23.2143, 100.0),
            "identity": WeaponIdentity.Sentinel,
        },
        {
            "eigenvalues": (35.3211, 79.8165, 14.2857, 100.0),
            "identity": WeaponIdentity.Wingman,
        }
    ],
}
