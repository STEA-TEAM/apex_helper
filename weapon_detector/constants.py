from typing import Dict, List

from .types import AmmoType, AmmoInfo, WeaponInfo, Polygon, Point

ORIGIN_SCREEN_SIZE = 3840
WEAPON_ICON_DICT: Dict[AmmoType, Polygon] = {
    AmmoType.Heavy: [(74, 4), (400, 4), (400, 91), (74, 91)],
    AmmoType.Light: [(74, 4), (400, 4), (400, 91), (74, 91)],
    AmmoType.Energy: [(74, 4), (400, 4), (400, 91), (74, 91)],
    AmmoType.Shotgun: [(74, 4), (400, 4), (400, 91), (74, 91)],
    AmmoType.Sniper: [(74, 4), (400, 4), (400, 91), (74, 91)],
    AmmoType.Mythic: [(74, 4), (400, 4), (400, 91), (74, 91)],
    AmmoType.Sheila: [(74, 4), (400, 4), (400, 91), (74, 91)],
    AmmoType.Sentry: [(74, 4), (400, 4), (400, 91), (74, 91)],
}
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
            "name": "rampage",
            "eigenvalues": (0.914, 0.759, 0.232),
        },
        {
            "name": "prowler",
            "eigenvalues": (0.469, 0.851, 0.269),
        },
        {
            "name": "flatline",
            "eigenvalues": (0.847, 0.862, 0.145),
        },
        {
            "name": "car",
            "eigenvalues": (0.745, 0.816, 0.181),
        },
        {
            "name": "3030",
            "eigenvalues": (0.929, 0.667, 0.156),
        }
    ],
    AmmoType.Light: [
        {
            "name": "g7",
            "eigenvalues": (0.880, 0.782, 0.201),
        },
        {
            "name": "spitfire",
            "eigenvalues": (0.856, 0.874, 0.185),
        },
        {
            "name": "r301",
            "eigenvalues": (0.794, 0.828, 0.150),
        },
        {
            "name": "r99",
            "eigenvalues": (0.709, 0.885, 0.143),
        },
        {
            "name": "p2020",
            "eigenvalues": (0.365, 0.770, 0.130),
        },
        {
            "name": "alternator",
            "eigenvalues": (0.380, 0.828, 0.278),
        },
        {
            "name": "car",
            "eigenvalues": (0.745, 0.816, 0.181),
        },
        {
            "name": "re45",
            "eigenvalues": (0.399, 0.874, 0.223),
        }
    ],
    AmmoType.Energy: [
        {
            "name": "volt",
            "eigenvalues": (0.635, 0.747, 0.231),
        },
        {
            "name": "triple",
            "eigenvalues": (0.933, 0.897, 0.196),
        },
        {
            "name": "devotion",
            "eigenvalues": (0.883, 0.793, 0.224),
        },
        {
            "name": "nemesis",
            "eigenvalues": (0.871, 0.793, 0.247),
        },
        {
            "name": "havoc",
            "eigenvalues": (0.782, 0.828, 0.212),
        }
    ],
    AmmoType.Shotgun: [
        {
            "name": "mozambique",
            "eigenvalues": (0.475, 0.805, 0.256),
        },
        {
            "name": "peacekeeper",
            "eigenvalues": (0.853, 0.839, 0.189),
        },
        {
            "name": "mastiff",
            "eigenvalues": (0.948, 0.782, 0.244),
        },
        {
            "name": "eva8",
            "eigenvalues": (0.819, 0.862, 0.173),
        }
    ],
    AmmoType.Sniper: [
        {
            "name": "charge",
            "eigenvalues": (0.764, 0.885, 0.311),
        },
        {
            "name": "longbow",
            "eigenvalues": (0.920, 0.667, 0.230),
        },
        {
            "name": "sentinel",
            "eigenvalues": (0.969, 0.747, 0.225),
        },
        {
            "name": "wingman",
            "eigenvalues": (0.445, 0.839, 0.288),
        }
    ],
    AmmoType.Mythic: [
        {
            "name": "hemlok",
            "eigenvalues": (0.791, 0.897, 0.176),
        },
        {
            "name": "bocek",
            "eigenvalues": (0.853, 0.839, 0.082),
        },
        {
            "name": "lstar",
            "eigenvalues": (0.706, 0.874, 0.393),
        },
        {
            "name": "kraber",
            "eigenvalues": (0.975, 0.782, 0.173),
        },
        {
            "name": "knife",
            "eigenvalues": (0.975, 0.782, 0.173),
        }
    ],
    AmmoType.Sheila: [
        {
            "name": "sheila",
            "eigenvalues": (0.0, 0.0, 0.0),
        }
    ],
    AmmoType.Sentry: [
        {
            "name": "sentry",
            "eigenvalues": (0.0, 0.0, 0.0),
        }
    ]
}
