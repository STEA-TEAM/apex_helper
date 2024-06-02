import pyautogui
import cv2
import numpy as np
import time

import os

from datetime import datetime

ORIGIN_SCREEN_SIZE = 3840
IMAGE_FOLDER = "./scr/"

LEFT_SOLT = [37, 171]
RIGHT_SOLT = [640, 167]

AMMO_CAP = [452, 98, 547, 136]

ACC_SOLT = [50, 136, 65, 139]
ACC_SOLT_STEP = [56, 0, 56, 0]
MODE1_CHOSEN = [397, 90, 404, 97]
MODE2_CHOSEN = [413, 90, 420, 97]

WEAPON_IMAGE = [74, 4, 400, 91]

BIN_NUM = 10

COLOR_MAP = {
    0x386B59: (0, 1),
    0x21342D: (0, 0),
    0x7D542D: (1, 1),
    0x3C2A1C: (1, 0),
    0x5A6E28: (2, 1),
    0x2E371D: (2, 0),
    0x6B2007: (3, 1),
    0x30110A: (3, 0),
    0x4B408F: (4, 1),
    0x241F43: (4, 0),
    0xB20137: (5, 1),
    0x54121F: (5, 0),
    0xA13CA1: (6, 1),
    0x3C6EB2: (7, 1),
}

TYPE_MAP = [
    "Heavy",
    "Light",
    "Energy",
    "Shotgun",
    "Sniper",
    "Legendary",
    "Saila",
    "Cyber",
]

WEAPON_PROP = [
    # 0-Heavy
    [
        [0.914, 0.759, 0.232, "暴走轻机枪"],
        [0.469, 0.851, 0.269, "猎兽冲锋枪"],
        [0.847, 0.862, 0.145, "平行步枪"],
        [0.745, 0.816, 0.181, "CAR冲锋枪-重型子弹"],
        [0.929, 0.667, 0.156, "30-30连发枪"],
    ],
    # 1-Light
    [
        [0.880, 0.782, 0.201, "G7侦察枪"],
        [0.856, 0.874, 0.185, "喷火轻机枪"],
        [0.794, 0.828, 0.150, "R-301"],
        [0.709, 0.885, 0.143, "R99冲锋枪"],
        [0.365, 0.770, 0.130, "P2020手枪"],
        [0.380, 0.828, 0.278, "转换者冲锋枪"],
        [0.745, 0.816, 0.181, "CAR冲锋枪-轻型子弹"],
        [0.399, 0.874, 0.223, "RE-45"],
    ],
    # 2-Energy
    [
        [0.635, 0.747, 0.231, "电能冲锋枪"],
        [0.933, 0.897, 0.196, "三重式狙击步枪"],
        [0.883, 0.793, 0.224, "专注轻机枪"],
        [0.871, 0.793, 0.247, "复仇女神"],
        [0.782, 0.828, 0.212, "哈沃克步枪"],
    ],
    # 3-Shotgun
    [
        [0.475, 0.805, 0.256, "莫桑比克"],
        [0.853, 0.839, 0.189, "和平捍卫者"],
        [0.948, 0.782, 0.244, "敖犬霰弹枪"],
        [0.819, 0.862, 0.173, "EVA-8"],
    ],
    # 4-Sniper
    [
        [0.764, 0.885, 0.311, "充能步枪"],
        [0.920, 0.667, 0.230, "长弓狙击步枪"],
        [0.969, 0.747, 0.225, "哨兵狙击步枪"],
        [0.445, 0.839, 0.288, "小帮手"],
    ],
    # 5-Legendary
    [
        [0.791, 0.897, 0.176, "赫姆洛克突击步枪"],
        [0.853, 0.839, 0.082, "波塞克复合弓"],
        [0.706, 0.874, 0.393, "L-Star"],
        [0.975, 0.782, 0.173, "克雷贝尔狙击枪"],
        [0.709, 0.494, 0.279, "手感舒适的刀刃"],
    ],
    [0, 0, 0, "塞拉转轮机枪"],
    [0, 0, 0, "赛博狙"],
    [0, 0, 0, "无武器或窗口异常"],
]

WEAPON_DATA = {
    "暴走轻机枪": [2, [2, 0, 1, 5], [], ["火力全开", 0xFF0004]],
    "猎兽冲锋枪": [2, [3, 0, 1, 5], [], []],
    "平行步枪": [2, [0, 1, 5], ["连发模式", "单发模式"], []],
    "CAR冲锋枪-重型子弹": [2, [0, 1, 5], [], []],
    "30-30连发枪": [2, [0, 1, 6, 7], [], []],
    "G7侦察枪": [2, [2, 0, 1, 6, 10], [], []],
    "喷火轻机枪": [2, [0, 1, 5], [], []],
    "R-301": [2, [3, 0, 1, 5], ["连发模式", "单发模式"], []],
    "R99冲锋枪": [2, [3, 0, 1, 5], [], []],
    "P2020手枪": [2, [3, 0, 1, 9], [], []],
    "转换者冲锋枪": [2, [3, 0, 1, 5], [], []],
    "CAR冲锋枪-轻型子弹": [2, [0, 1, 3], [], []],
    "RE-45": [2, [3, 0, 1, 9], [], []],
    "电能冲锋枪": [2, [3, 0, 1, 5], [], []],
    "三重式狙击步枪": [2, [0, 1, 6], [], []],
    "专注轻机枪": [2, [2, 0, 1, 5, 8], [], []],
    "复仇女神": [2, [2, 0, 1, 5], [], []],
    "哈沃克步枪": [2, [0, 1, 5, 8], [], []],
    "莫桑比克": [2, [4, 1, 9], [], []],
    "和平捍卫者": [2, [4, 1, 5], ["收束器开启", "收束器关闭"], []],
    "敖犬霰弹枪": [2, [4, 1, 5], [], []],
    "EVA-8": [2, [4, 1, 5, 10], [], []],
    "充能步枪": [2, [1, 6], [], []],
    "长弓狙击步枪": [2, [2, 0, 1, 6, 7], [], []],
    "哨兵狙击步枪": [2, [0, 1, 6], [], ["充能状态", 0x86FFDD]],
    "小帮手": [2, [0, 1, 7], [], []],
    "赫姆洛克突击步枪": [2, [1], ["三连发模式", "单发模式"], []],
    "波塞克复合弓": [3, [1], [], []],
    "L-Star": [3, [1], [], []],
    "克雷贝尔狙击枪": [2, [], [], []],
    "手感舒适的刀刃": [2, [], [], []],
}

ACC_COLOR = [
    [75, 75, 75],
    [221, 221, 221],
    [46, 188, 255],
    [222, 107, 255],
    [255, 226, 0],
    [255, 69, 69],
]

ACC_NAME = [
    "弹夹",
    "瞄准镜",
    "枪管稳定器",
    "激光瞄准镜",
    "霰弹枪栓",
    "标准枪托",
    "狙击枪托",
    "穿颅器",
    "涡轮增压器",
    "锤击点子弹",
    "双发扳机",
]

AMMO_LOAD_POS = [
    [4, 42],
    [4, 34],
    [4, 19],
    [20, 4],
    [20, 17],
    [20, 53],
    [37, 11],
    [13, 20],
    [37, 40],
    [28, 37],
]

AMMO_LOAD_COL = []
AMMO_LOAD_ROW = []
for point in AMMO_LOAD_POS:
    AMMO_LOAD_COL.append(point[0])
    AMMO_LOAD_ROW.append(point[1])

AMMO_LOAD2 = [454, 21, 549, 80]
AMMO_LOAD3 = [401, 21, 549, 80]

AMMO_LOAD_SIZE = [42, 10]
AMMO_LOAD_DIGIT_MASK = [
    [255, 255, 255, 255, 0, 255, 255, 255, 255, 255],
    [0, 0, 0, 255, 255, 255, 0, 0, 0, 0],
    [255, 0, 0, 255, 0, 255, 255, 0, 0, 0],
    [255, 0, 0, 255, 0, 255, 255, 0, 255, 0],
    [0, 0, 255, 0, 0, 0, 255, 0, 255, 0],
    [255, 0, 255, 255, 0, 255, 0, 0, 255, 0],
    [255, 255, 255, 255, 0, 255, 0, 0, 255, 0],
    [255, 0, 0, 255, 0, 0, 255, 0, 0, 0],
    [255, 255, 255, 255, 0, 255, 255, 0, 255, 0],
    [255, 0, 255, 255, 0, 255, 255, 0, 255, 0],
]


def get_point_color(img, point):
    # print("Color Point Position: ", point)
    point = img[point[1], point[0]]
    ret = (point[2] << 16) + (point[1] << 8) + point[0]
    # print("Color: ", hex(ret))
    return ret


def get_part(img, pos):
    ret = img[pos[1] : pos[3], pos[0] : pos[2]]
    # cv2.imshow("part", ret)
    return ret


def stat_weapon_image(img):
    ratio = 255
    weapon = cv2.subtract(get_part(img, WEAPON_IMAGE), (254, 254, 254, 0)) * ratio
    # cv2.imshow("img", weapon)
    # strip
    weapon_board = [0, 0, 0, 0]
    for col in range(weapon.shape[1]):
        # print(col, np.sum(weapon[:, col]))
        if np.sum(weapon[:, col]):
            weapon_board[0] = col
            break

    for col in range(weapon.shape[1] - 1, 0, -1):
        # print(col, np.sum(weapon[:, col]))
        if np.sum(weapon[:, col]):
            weapon_board[2] = col
            break

    for row in range(weapon.shape[0]):
        if np.sum(weapon[row, :]):
            weapon_board[1] = row
            break

    for row in range(weapon.shape[0] - 1, 0, -1):
        if np.sum(weapon[row, :]):
            weapon_board[3] = row
            break

    # print(weapon_board)
    Height = weapon_board[3] - weapon_board[1]
    Length = weapon_board[2] - weapon_board[0]
    weapon = weapon[
        weapon_board[1] : weapon_board[3], weapon_board[0] : weapon_board[2]
    ]
    lr = np.round(Length / (WEAPON_IMAGE[2] - WEAPON_IMAGE[0]), 3)
    hr = np.round(Height / (WEAPON_IMAGE[3] - WEAPON_IMAGE[1]), 3)
    sr = np.round(np.sum(weapon) / Length / Height / 3 / ratio, 3)
    # print("Weapon Length:", lr))
    # print("Weapon Height:", hr)
    # print("Weapon Ratio:", sr)
    # print(lr, hr, sr)
    # cv2.imshow("img", weapon)
    return (lr, hr, sr)


def get_weapon_type(img):
    try:
        left_type = COLOR_MAP[get_point_color(img, LEFT_SOLT)]
    except KeyError:
        left_type = [0, 0]
        # print("No Weapon in Left Solt")
    try:
        right_type = COLOR_MAP[get_point_color(img, RIGHT_SOLT)]
    except KeyError:
        right_type = [0, 0]
        # print("No Weapon in Right Solt")
    select = []
    if left_type[1] == 1:
        select = [left_type[0], "Left"]
    elif right_type[1] == 1:
        select = [right_type[0], "Right"]
    else:
        # print("No Weapon or Error")
        return 8
    # print("Left: %s, Right: %s Select: %s" % (TYPE_MAP[left_type[0]], TYPE_MAP[right_type[0]], select[1]))
    return select[0]


def get_weapon(img, weapon_type):
    if weapon_type > 5:
        res = WEAPON_PROP[weapon_type][3]
    else:
        prop = stat_weapon_image(img)
        comp_res = []
        LR_VALUE = 1
        HR_VALUE = 1
        SR_VALUE = 1
        for weapon in WEAPON_PROP[weapon_type]:
            comp_res.append(
                abs(prop[0] - weapon[0])
                + abs(prop[1] - weapon[1])
                + abs(prop[2] - weapon[2])
            )
        # print(comp_res)
        res = WEAPON_PROP[weapon_type][comp_res.index(min(comp_res))][3]
        # print(res)
    return res


def get_ammo_load(img, width=2):
    if width == 2:
        ammo_img = get_part(img, AMMO_LOAD2)
    elif width == 3:
        ammo_img = get_part(img, AMMO_LOAD3)
    ref_color = ammo_img[-1, 0]
    # print(ammo_img)
    # print("Reference Color:", ref_color)
    ammo_img = ammo_img.astype("int16")
    ammo_cont = np.sum(np.abs(ammo_img - ref_color), axis=2)
    threshold_cont = (np.max(ammo_cont) - np.min(ammo_cont)) * 0.85
    # print("Threshold Contrast:", threshold_cont)
    ammo_img = np.where(ammo_cont > threshold_cont, 255, 0).astype("uint8")
    # cv2.imshow("ammo2", ammo2)
    # cv2.imwrite(IMAGE_FOLDER + "ammo_load/ammo41.bmp", ammo2)
    ammo_load = 0
    left_pos = 0

    # firsr digit
    digit_img = ammo_img[:, left_pos : left_pos + AMMO_LOAD_SIZE[0]]
    res = np.abs(
        np.array(AMMO_LOAD_DIGIT_MASK)
        - digit_img[AMMO_LOAD_ROW, AMMO_LOAD_COL].flatten()
    )
    res = np.sum(np.where(res == 255, 1, 0), axis=1)
    # print(res)
    if np.min(res) < 2:
        ammo_load += 10 * np.argmin(res)
    left_pos += AMMO_LOAD_SIZE[0] + AMMO_LOAD_SIZE[1]

    # second digit
    digit_img = ammo_img[:, left_pos : left_pos + AMMO_LOAD_SIZE[0]]
    res = np.abs(
        np.array(AMMO_LOAD_DIGIT_MASK)
        - digit_img[AMMO_LOAD_ROW, AMMO_LOAD_COL].flatten()
    )
    res = np.sum(np.where(res == 255, 1, 0), axis=1)
    # print(digit_img[AMMO_LOAD_ROW, AMMO_LOAD_COL].flatten())
    if np.min(res) < 2:
        ammo_load += np.argmin(res)
    left_pos += AMMO_LOAD_SIZE[0] + AMMO_LOAD_SIZE[1]

    # third digit
    if width == 3:
        digit_img = ammo_img[:, left_pos : left_pos + AMMO_LOAD_SIZE[0]]
        res = np.abs(
            np.array(AMMO_LOAD_DIGIT_MASK)
            - digit_img[AMMO_LOAD_ROW, AMMO_LOAD_COL].flatten()
        )
        res = np.sum(np.where(res == 255, 1, 0), axis=1)
        if np.min(res) < 2:
            ammo_load = 10 * ammo_load + np.argmin(res)
    # print(res)

    # print("Ammo Loaded:", ammo_load)
    return ammo_load


def get_accessory(img, acc_solt_num):
    acc_list = []
    acc_part_pos = np.array(ACC_SOLT.copy())
    for acc in range(acc_solt_num):
        acc_img = get_part(img, acc_part_pos)
        # cv2.imshow("acc", acc_img)
        # print(acc_img)
        acc_color = np.average(acc_img, axis=(0, 1)).astype("uint8")
        delta_arr = np.abs((np.array(ACC_COLOR) - np.flipud(acc_color)))
        # May need LOG Weighting
        delta_arr = np.sum(delta_arr, axis=1)
        acc_type = np.argmin(delta_arr)
        # print("ACC Slot: ", delta_arr, acc_type)
        acc_list.append(acc_type)
        acc_part_pos += ACC_SOLT_STEP
    return acc_list


def get_fire_mode(img):
    mode1_img = np.sum(get_part(img, MODE1_CHOSEN))
    mode2_img = np.sum(get_part(img, MODE2_CHOSEN))
    ret = 1 if (mode1_img > mode2_img) else 2
    print("Fire Mode:", ret)
    return ret


if __name__ == "__main__":

    # Get Screen Size
    screen_size = pyautogui.size()
    print(f"Screen size: {screen_size}")

    # Get Scale
    scale = screen_size[0] / ORIGIN_SCREEN_SIZE
    # time.sleep(1)
    # Get wwapon area
    area_width = round(731 * scale)
    area_height = round(207 * scale)
    area_pos = (
        screen_size[0] - area_width - round(101 * scale),
        screen_size[1] - area_height - round(45 * scale),
        area_width,
        area_height,
    )

    # cv2.waitKey(0)
    # cv2.imshow("scrshot", cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
    # cv2.imwrite(IMAGE_FOLDER + "1.bmp", cv2.cvtColor(np.asarray(pyautogui.screenshot(region=area_pos)), cv2.COLOR_RGB2BGR))

    # Working Code
    while True:
        # print("Begin  :", datetime.now())
        img = cv2.cvtColor(
            np.asarray(pyautogui.screenshot(region=area_pos)), cv2.COLOR_RGB2BGR
        )
        img = cv2.resize(img, (round(area_pos[2] / scale), round(area_pos[3] / scale)))
        # print("Capture:", datetime.now())
        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        weapon_type = get_weapon_type(img)
        res = get_weapon(img, weapon_type)
        ammo_load = get_ammo_load(img, WEAPON_DATA[res][0])
        acc_level = get_accessory(img, len(WEAPON_DATA[res][1]))
        acc_info = ""
        for acc in range(len(WEAPON_DATA[res][1])):
            acc_info += (
                ACC_NAME[WEAPON_DATA[res][1][acc]]
                + " - Lv."
                + str(acc_level[acc])
                + " "
            )
        print("Result :", res, end=" ")
        print("Ammo :", ammo_load, end=" ")
        print("Acc Info:", acc_info)

    # Develop, end = " "
    # img = cv2.imread(IMAGE_FOLDER + "l2.bmp")
    # print("Load Complete")

    # Fire Mode
    # get_fire_mode(img)
    # Accessory
    # get_accessory(img, 2)

    # Weapon
    # weapon_type = get_weapon_type(img)
    # get_weapon(img, weapon_type)
    # Ammo Load
    # get_ammo_load(img, 3)

    # Ammo Cap
    #     ammo_img = get_part(img, AMMO_CAP)
    #     #print(ammo_img)
    #     #cv2.imshow("ammo", ammo_img)
    #     #cv2.waitKey(0)
    #     ammo_img = ammo_img.astype("uint16")
    #     ammo_img = np.sum(ammo_img, axis = 2)
    #     BIN_NUM = 20
    #     ammo_hist = np.histogram(ammo_img.flatten(), bins = BIN_NUM)
    #     print(ammo_hist)
    #     plt.hist(ammo_img.flatten(),bins=BIN_NUM,color='red')
    #     plt.show()
    #     #print(ammo_img)
    #     ammo_img = np.where(ammo_img > 230, 255, 0).astype("uint8")
    #     #print(ammo_img)

    #     ammo_img = cv2.cvtColor(ammo_img,cv2.COLOR_BGR2GRAY)
    #     ammo_img = cv2.adaptiveThreshold(
    #         ammo_img,
    #         maxValue=255,
    #         adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
    #         thresholdType=cv2.THRESH_BINARY,
    #         blockSize=11,
    #         C=1)
    # cv2.imshow("ammo2", ammo_img)
    cv2.waitKey(0)

# For Getting Data

# img = cv2.imread('C:/Users/CafuuChino/Desktop/Apex/scr/ammo_load/0.bmp')
# sum = np.zeros((img.shape[0], img.shape[1]))

# file = r'C:/Users/CafuuChino/Desktop/Apex/scr/ammo_load'
# file = r'C:/Users/CafuuChino/Desktop/Apex/scr'
# for root, dirs, files in os.walk(file):
#     if root != file:
#             break
#     for file in files:
#         path = os.path.join(root, file)
#         print(file, end = " ")
#         img = cv2.imread(path)

#         # build AMMO_LOAD_MASK
#         # img = np.sum(img, axis = 2)
#         # img = np.where(img > 100, 255, 0)
#         # #sum += img
#         # print(img[AMMO_LOAD_ROW, AMMO_LOAD_COL].flatten())
#         get_ammo_load(img, 2)


# #sum = np.where(sum == 255, 255, 0).astype("uint8")
# print(sum)
# #cv2.imwrite(IMAGE_FOLDER + '/ammo_load/' + 'sum.bmp', sum)
# cv2.imshow("sum", sum)
# cv2.waitKey(0)
#              cv2.imwrite(IMAGE_FOLDER + '/ammo_load/' + file[-5] + '.bmp', img[:, 53:])
#              #stat_weapon_image(img)
#     cv2.destroyAllWindows()
