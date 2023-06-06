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
    AmmoType.Heavy: [
        {
            "name": "3030",
            "eigenvalues": (93.1193, 69.6429, 9.6412),
        },
        {
            "name": "car",
            "eigenvalues": (74.3119, 85.7143, 10.059),
        },
        {
            "name": "flatline",
            "eigenvalues": (74.7706, 87.5, 9.4692),
        },
        {
            "name": "hemlok",
            "eigenvalues": (72.0183, 89.2857, 11.7464),
        },
        {
            "name": "prowler",
            "eigenvalues": (0.4725, 0.8448, 0.0982),
        },
        {
            "name": "rampage",
            "eigenvalues": (91.2844, 76.7857, 14.8263),
        },

    ],
    AmmoType.Light: [
        {
            "name": "alternator",
            "eigenvalues": (38.5321, 83.9286, 8.0111),
        },
        {
            "name": "car",
            "eigenvalues": (74.3119, 85.7143, 10.059),
        },
        {
            "name": "g7",
            "eigenvalues": (86.6972, 80.3571, 12.8768),
        },
        {
            "name": "p2020",
            "eigenvalues": (35.7798, 78.5714, 3.1701),
        },
        {
            "name": "r301",
            "eigenvalues": (74.3119, 83.9286, 9.502),
        },
        {
            "name": "r99",
            "eigenvalues": (71.1009, 89.2857, 8.134),
        },
        {
            "name": "re45",
            "eigenvalues": (39.9083, 89.2857, 7.2985),
        },
        {
            "name": "spitfire",
            "eigenvalues": (85.3211, 91.0714, 12.8358),
        },
    ],
    AmmoType.Energy: [
        {
            "name": "devotion",
            "eigenvalues": (88.5321, 80.3571, 14.9738),
        },
        {
            "name": "havoc",
            "eigenvalues": (78.4404, 87.5, 12.7048),
        },
        {
            "name": "lstar",
            "eigenvalues": (70.1835, 87.5, 22.8784),
        },
        {
            "name": "nemesis",
            "eigenvalues": (87.156, 80.3571, 15.9486),
        },
        {
            "name": "triple",
            "eigenvalues": (93.1193, 91.0714, 14.9001),
        },
        {
            "name": "volt",
            "eigenvalues": (63.7615, 75.0, 10.4194),
        },
    ],
    AmmoType.Shotgun: [
        {
            "name": "eva8",
            "eigenvalues": (81.6514, 87.5, 11.2303),
        },
        {
            "name": "mastiff",
            "eigenvalues": (94.9541, 78.5714, 17.4803),
        },
        {
            "name": "mozambique",
            "eigenvalues": (47.7064, 78.5714, 9.9689),
        },
        {
            "name": "peacekeeper",
            "eigenvalues": (85.3211, 76.7857, 12.4754),
        },
    ],
    AmmoType.Sniper: [
        {
            "name": "charge",
            "eigenvalues": (76.1468, 89.2857, 19.8067),
        },
        {
            "name": "longbow",
            "eigenvalues": (91.7431, 69.6429, 13.3109),
        },
        {
            "name": "sentinel",
            "eigenvalues": (96.789, 73.2143, 15.4489),
        },
        {
            "name": "wingman",
            "eigenvalues": (44.4954, 83.9286, 10.018),
        }
    ],
    AmmoType.Mythic: [
        {
            "name": "bocek",
            "eigenvalues": (84.8624, 87.5, 5.4718),
        },
        {
            "name": "hemlok",
            "eigenvalues": (72.0183, 89.2857, 11.7464),
        },
        {
            "name": "knife",
            "eigenvalues": (72.2009, 52.7857, 9.7067),
        },
        {
            "name": "kraber",
            "eigenvalues": (97.2477, 82.1429, 12.6065),
        },
        {
            "name": "lstar",
            "eigenvalues": (70.1835, 87.5, 22.8784),
        },
    ],
    AmmoType.Sheila: [
        {
            "name": "sheila",
            "eigenvalues": (92.2018, 91.0714, 32.5442),
        }
    ],
    AmmoType.Sentry: [
        {
            "name": "sentry",
            "eigenvalues": (95.4128, 80.3571, 13.5239),
        }
    ]
}
