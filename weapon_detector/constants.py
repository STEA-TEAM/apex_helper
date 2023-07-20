from typing import Dict, List
from .types import AmmoType, AmmoInfo, WeaponInfo, Point, Rectangle

ORIGIN_SCREEN_SIZE = 3840
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
    0x5a6e28: {
        "type": AmmoType.Energy,
        "active": True
    },
    0x2e371d: {
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
    0x4b408f: {
        "type": AmmoType.Sniper,
        "active": True
    },
    0x241f43: {
        "type": AmmoType.Sniper,
        "active": False
    },
    0xb20137: {
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
            "name": "devotion",
            "eigenvalues": (11.4679, 100.0, 17.8571, 100.0),
        },
        {
            "name": "havoc",
            "eigenvalues": (15.5963, 94.0367, 12.5, 100.0),
        },
        {
            "name": "lstar",
            "eigenvalues": (21.5596, 92.2018, 12.5, 100.0),
        },
        {
            "name": "nemesis",
            "eigenvalues": (11.0092, 98.1651, 19.6429, 100.0),
        },
        {
            "name": "triple",
            "eigenvalues": (6.8807, 100.0, 7.1429, 100.0),
        },
        {
            "name": "volt",
            "eigenvalues": (23.8532, 87.6147, 25.0, 100.0),
        },
    ],
    AmmoType.Heavy: [
        {
            "name": "3030",
            "eigenvalues": (6.8807, 100.0, 23.2143, 94.6429),
        },
        {
            "name": "car",
            "eigenvalues": (19.2661, 93.578, 10.7143, 98.2143),
        },
        {
            "name": "flatline",
            "eigenvalues": (15.5963, 91.7431, 12.5, 100.0),
        },
        {
            "name": "hemlok",
            "eigenvalues": (19.7248, 92.6606, 7.1429, 100.0),
        },
        {
            "name": "prowler",
            "eigenvalues": (36.2385, 84.4037, 12.5, 100.0),
        },
        {
            "name": "rampage",
            "eigenvalues": (8.7156, 100.0, 23.2143, 100.0),
        },

    ],
    AmmoType.Light: [
        {
            "name": "alternator",
            "eigenvalues": (39.9083, 78.4404, 14.2857, 100.0),
        },
        {
            "name": "car",
            "eigenvalues": (19.2661, 93.578, 10.7143, 98.2143),
        },
        {
            "name": "g7",
            "eigenvalues": (11.9266, 100.0, 14.2857, 98.2143),
        },
        {
            "name": "p2020",
            "eigenvalues": (37.6147, 74.7706, 21.4286, 100.0),
        },
        {
            "name": "r301",
            "eigenvalues": (20.1835, 94.9541, 16.0714, 100.0),
        },
        {
            "name": "r99",
            "eigenvalues": (25.2294, 96.3303, 10.7143, 100.0),
        },
        {
            "name": "re45",
            "eigenvalues": (38.0734, 77.9817, 10.7143, 100.0),
        },
        {
            "name": "spitfire",
            "eigenvalues": (13.7615, 99.0826, 7.1429, 100.0),
        },
    ],
    AmmoType.Mythic: [
        {
            "name": "bocek",
            "eigenvalues": (11.4679, 97.2477, 10.7143, 98.2143),
        },
        {
            "name": "hemlok",
            "eigenvalues": (19.7248, 92.6606, 7.1429, 100.0),
        },
        {
            "name": "knife",
            "eigenvalues": (20.6422, 92.2018, 28.5714, 80.3571),
        },
        {
            "name": "kraber",
            "eigenvalues": (2.2936, 100.0, 16.0714, 98.2143),
        },
        {
            "name": "lstar",
            "eigenvalues": (21.5596, 92.2018, 12.5, 100.0),
        },
    ],
    AmmoType.Sentry: [
        {
            "name": "sentry",
            "eigenvalues": (4.1284, 100.0, 14.2857, 98.2143),
        }
    ],
    AmmoType.Sheila: [
        {
            "name": "sheila",
            "eigenvalues": (3.211, 95.8716, 7.1429, 100.0),
        }
    ],
    AmmoType.Shotgun: [
        {
            "name": "eva8",
            "eigenvalues": (17.8899, 99.5413, 12.5, 100.0),
        },
        {
            "name": "mastiff",
            "eigenvalues": (5.0459, 100.0, 19.6429, 100.0),
        },
        {
            "name": "mozambique",
            "eigenvalues": (32.1101, 79.8165, 17.8571, 100.0),
        },
        {
            "name": "peacekeeper",
            "eigenvalues": (14.6789, 100.0, 14.2857, 92.8571),
        },
    ],
    AmmoType.Sniper: [
        {
            "name": "charge",
            "eigenvalues": (17.8899, 94.0367, 8.9286, 100.0),
        },
        {
            "name": "longbow",
            "eigenvalues": (7.7982, 100.0, 19.6429, 91.0714),
        },
        {
            "name": "sentinel",
            "eigenvalues": (3.211, 100.0, 23.2143, 100.0),
        },
        {
            "name": "wingman",
            "eigenvalues": (35.3211, 79.8165, 14.2857, 100.0),
        }
    ],
}
