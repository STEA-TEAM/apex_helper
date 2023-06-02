from typing import TypedDict

from types import AmmoInfo

ORIGIN_SCREEN_SIZE = 3840
LEFT_SOLT = (37, 171)
RIGHT_SOLT = (640, 167)

AMMO_COLOR_DICT: TypedDict[int, AmmoInfo] = {
    0x386B59: {
        "type": "heavy",
        "active": True
    },
    0x21342d: {
        "type": "heavy",
        "active": False
    },
    0x7d542d: {
        "type": "light",
        "active": True
    },
    0x3c2a1c: {
        "type": "light",
        "active": False
    },
    0x5a6e28: {
        "type": "energy",
        "active": True
    },
    0x2e371d: {
        "type": "energy",
        "active": False
    },
    0x6b2007: {
        "type": "shotgun",
        "active": True
    },
    0x30110a: {
        "type": "shotgun",
        "active": False
    },
    0x4b408f: {
        "type": "sniper",
        "active": True
    },
    0x241f43: {
        "type": "sniper",
        "active": False
    },
    0xb20137: {
        "type": "mythic",
        "active": True
    },
    0x54121f: {
        "type": "mythic",
        "active": False
    },
    0xa13ca1: {
        "type": "sheila",
        "active": True
    },
    0x3c6eb2: {
        "type": "sentry",
        "active": True
    },
}

WEAPON_TYPE_DICT = {
    "heavy": {
        "rampage": {
            "name": "暴走轻机枪",
            "eigenvalues": [0.914, 0.759, 0.232],
        },
        "prowler": {
            "name": "猎兽冲锋枪",
            "eigenvalues": [0.469, 0.851, 0.269],
        },
        "flatline": {
            "name": "平行步枪",
            "eigenvalues": [0.847, 0.862, 0.145],
        },
        "car": {
            "name": "CAR冲锋枪-重型子弹",
            "eigenvalues": [0.745, 0.816, 0.181],
        },
        "3030": {
            "name": "30-30连发枪",
            "eigenvalues": [0.929, 0.667, 0.156],
        }
    },
    "light": {
        "g7": {
            "name": "G7侦察枪",
            "eigenvalues": [0.880, 0.782, 0.201],
        },
        "spitfire": {
            "name": "喷火轻机枪",
            "eigenvalues": [0.856, 0.874, 0.185],
        },
        "r301": {
            "name": "R-301",
            "eigenvalues": [0.794, 0.828, 0.150],
        },
        "r99": {
            "name": "R99冲锋枪",
            "eigenvalues": [0.709, 0.885, 0.143],
        },
        "p2020": {
            "name": "P2020手枪",
            "eigenvalues": [0.365, 0.770, 0.130],
        },
        "alternator": {
            "name": "转换者冲锋枪",
            "eigenvalues": [0.380, 0.828, 0.278],
        },
        "car": {
            "name": "CAR冲锋枪-轻型子弹",
            "eigenvalues": [0.745, 0.816, 0.181],
        },
        "re45": {
            "name": "RE-45",
            "eigenvalues": [0.399, 0.874, 0.223],
        }
    },
    "energy": {
        "volt": {
            "name": "电能冲锋枪",
            "eigenvalues": [0.635, 0.747, 0.231],
        },
        "triple": {
            "name": "三重式狙击步枪",
            "eigenvalues": [0.933, 0.897, 0.196],
        },
        "devotion": {
            "name": "专注轻机枪",
            "eigenvalues": [0.883, 0.793, 0.224],
        },
        "nemesis": {
            "name": "复仇女神",
            "eigenvalues": [0.871, 0.793, 0.247],
        },
        "havoc": {
            "name": "哈沃克步枪",
            "eigenvalues": [0.782, 0.828, 0.212],
        }
    },
    "shotgun": {
        "mozambique": {
            "name": "莫桑比克",
            "eigenvalues": [0.475, 0.805, 0.256],
        },
        "peacekeeper": {
            "name": "和平捍卫者",
            "eigenvalues": [0.853, 0.839, 0.189],
        },
        "mastiff": {
            "name": "敖犬霰弹枪",
            "eigenvalues": [0.948, 0.782, 0.244],
        },
        "eva8": {
            "name": "EVA-8",
            "eigenvalues": [0.819, 0.862, 0.173],
        }
    },
    "sniper": {
        "charge": {
            "name": "充能步枪",
            "eigenvalues": [0.764, 0.885, 0.311],
        },
        "longbow": {
            "name": "长弓狙击步枪",
            "eigenvalues": [0.920, 0.667, 0.230],
        },
        "sentinel": {
            "name": "哨兵狙击步枪",
            "eigenvalues": [0.969, 0.747, 0.225],
        },
        "wingman": {
            "name": "小帮手",
            "eigenvalues": [0.445, 0.839, 0.288],
        }
    },
    "mythic": {
        "hemlok": {
            "name": "赫姆洛克突击步枪",
            "eigenvalues": [0.791, 0.897, 0.176],
        },
        "bocek": {
            "name": "波塞克复合弓",
            "eigenvalues": [0.853, 0.839, 0.082],
        },
        "lstar": {
            "name": "L-Star",
            "eigenvalues": [0.706, 0.874, 0.393],
        },
        "kraber": {
            "name": "克雷贝尔狙击枪",
            "eigenvalues": [0.975, 0.782, 0.173],
        },
        "kunai": {
            "name": "手感舒适的刀刃",
            "eigenvalues": [0.709, 0.494, 0.279],
        }
    },
    "sheila": {
        "sheila": {
            "name": "塞拉转轮机枪",
            "eigenvalues": [0, 0, 0],
        }
    },
    "sentry": {
        "sentry": {
            "name": "A-13 旧式哨兵",
            "eigenvalues": [0, 0, 0],
        }
    },
}