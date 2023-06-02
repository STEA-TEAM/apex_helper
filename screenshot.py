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

AMMO_LOAD = [452, 22, 549, 80]
AMMO_CAP = [452, 98, 547, 146]
ACC_SOLT = [32, 92, 305, 141]

WEAPON_IMAGE = [74, 4, 400, 91]

COLOR_MAP = {
    0x386B59: (0, 1),
    0x21342d: (0, 0),
    0x7d542d: (1, 1),
    0x3c2a1c: (1, 0),
    0x5a6e28: (2, 1),
    0x2e371d: (2, 0),
    0x6b2007: (3, 1),
    0x30110a: (3, 0),
    0x4b408f: (4, 1),
    0x241f43: (4, 0),
    0xb20137: (5, 1),
    0x54121f: (5, 0),
    0xa13ca1: (6, 1),
    0x3c6eb2: (7, 1)
}

TYPE_MAP = ["Heavy", "Light", "Energy", "Shotgun", "Sniper", "Legendary", "Saila", "Cyber"]

WEAPON_PROP = [
    # 0-Heavy
    [
        [0.914, 0.759, 0.232, "暴走轻机枪"],
        [0.469, 0.851, 0.269, "猎兽冲锋枪"],
        [0.847, 0.862, 0.145, "平行步枪"],
        [0.745, 0.816, 0.181, "CAR冲锋枪-重型子弹"],
        [0.929, 0.667, 0.156, "30-30连发枪"]],
    # 1-Light
    [
        [0.880, 0.782, 0.201, "G7侦察枪"],
        [0.856, 0.874, 0.185, "喷火轻机枪"],
        [0.794, 0.828, 0.150, "R-301"],
        [0.709, 0.885, 0.143, "R99冲锋枪"],
        [0.365, 0.770, 0.130, "P2020手枪"],
        [0.380, 0.828, 0.278, "转换者冲锋枪"],
        [0.745, 0.816, 0.181, "CAR冲锋枪-轻型子弹"],
        [0.399, 0.874, 0.223, "RE-45"]],
    # 2-Energy
    [
        [0.635, 0.747, 0.231, "电能冲锋枪"],
        [0.933, 0.897, 0.196, "三重式狙击步枪"],
        [0.883, 0.793, 0.224, "专注轻机枪"],
        [0.871, 0.793, 0.247, "复仇女神"],
        [0.782, 0.828, 0.212, "哈沃克步枪"]],
    # 3-Shotgun
    [
        [0.475, 0.805, 0.256, "莫桑比克"],
        [0.853, 0.839, 0.189, "和平捍卫者"],
        [0.948, 0.782, 0.244, "敖犬霰弹枪"],
        [0.819, 0.862, 0.173, "EVA-8"]],
    # 4-Sniper
    [
        [0.764, 0.885, 0.311, "充能步枪"],
        [0.920, 0.667, 0.230, "长弓狙击步枪"],
        [0.969, 0.747, 0.225, "哨兵狙击步枪"],
        [0.445, 0.839, 0.288, "小帮手"]],
    # 5: Legendary
    [
        [0.791, 0.897, 0.176, "赫姆洛克突击步枪"],
        [0.853, 0.839, 0.082, "波塞克复合弓"],
        [0.706, 0.874, 0.393, "L-Star"],
        [0.975, 0.782, 0.173, "克雷贝尔狙击枪"],
        [0.709, 0.494, 0.279, "手感舒适的刀刃"]],
    # 6: Sheila
    [0, 0, 0, "塞拉转轮机枪"],
    # 7: A-13 Sentry
    [0, 0, 0, "赛博狙"]
]


def get_point_color(img, point):
    # print("Color Point Position: ", point)
    point = img[point[1], point[0]]
    ret = (point[2] << 16) + (point[1] << 8) + point[0]
    # print("Color: ", hex(ret))
    return ret


def get_part(img, pos):
    ret = img[pos[1]:pos[3], pos[0]:pos[2]]
    cv2.imshow("part", ret)
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
    weapon = weapon[weapon_board[1]: weapon_board[3], weapon_board[0]: weapon_board[2]]
    lr = np.round(Length / (WEAPON_IMAGE[2] - WEAPON_IMAGE[0]), 3)
    hr = np.round(Height / (WEAPON_IMAGE[3] - WEAPON_IMAGE[1]), 3)
    sr = np.round(np.sum(weapon) / Length / Height / 3 / ratio, 3)
    # print("Weapon Length:", lr))
    # print("Weapon Height:", hr)
    # print("Weapon Ratio:", sr)
    # print(lr, hr, sr)
    return (lr, hr, sr)
    # cv2.imshow("img", weapon)


def get_weapon_type(img):
    try:
        left_type = COLOR_MAP[get_point_color(img, LEFT_SOLT)]
    except KeyError:
        left_type = [0, 0]
        print("No Weapon in Left Solt")
    try:
        right_type = COLOR_MAP[get_point_color(img, RIGHT_SOLT)]
    except KeyError:
        right_type = [0, 0]
        print("No Weapon in Right Solt")
    select = []
    if left_type[1] == 1:
        select = [left_type[0], "Left"]
    elif right_type[1] == 1:
        select = [right_type[0], "Right"]
    else:
        print("No Weapon or Error")
    # print("Left: %s, Right: %s Select: %s" % (TYPE_MAP[left_type[0]], TYPE_MAP[right_type[0]], select[1]))
    return select[0]


def get_weapon(img, weapon_type):
    if weapon_type > 5:
        ret = WEAPON_PROP[weapon_type][4]
    else:
        prop = stat_weapon_image(img)
        comp_res = []
        LR_VALUE = 1
        HR_VALUE = 1
        SR_VALUE = 1
        for weapon in WEAPON_PROP[weapon_type]:
            comp_res.append(abs(prop[0] - weapon[0]) + abs(prop[1] - weapon[1]) + abs(prop[2] - weapon[2]))
        # print(comp_res)
        res = WEAPON_PROP[weapon_type][comp_res.index(min(comp_res))][3]

        # print(res)
        return res


if __name__ == '__main__':

    # Get Screen Size
    screen_size = pyautogui.size()
    print(f"Screen size: {screen_size}")

    # Get Scale
    scale = screen_size[0] / ORIGIN_SCREEN_SIZE
    # time.sleep(1)
    # Get wwapon area
    area_width = round(731 * scale)
    area_height = round(207 * scale)
    area_pos = (screen_size[0] - area_width - round(101 * scale),
                screen_size[1] - area_height - round(45 * scale),
                area_width,
                area_height
                )

    # cv2.waitKey(0)
    # cv2.imshow("scrshot", cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
    # cv2.imwrite(IMAGE_FOLDER + "1.bmp", cv2.cvtColor(np.asarray(pyautogui.screenshot(region=area_pos)), cv2.COLOR_RGB2BGR))

    # Working Code
    while True:
        # print("Begin  :", datetime.now())
        img = cv2.cvtColor(np.asarray(pyautogui.screenshot(region=area_pos)), cv2.COLOR_RGB2BGR)
        # print("Capture:", datetime.now())
        # cv2.imshow("img",img)
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     break

        weapon_type = get_weapon_type(img)
        res = get_weapon(img, weapon_type)
        print("Result : ", datetime.now(), res)

#     img = cv2.imread(IMAGE_FOLDER + "x4.bmp")
#     print("Load Complete")
#     ammo_img = cv2.cvtColor(get_part(img, AMMO_CAP),cv2.COLOR_BGR2GRAY)
# #     ammo_img = cv2.adaptiveThreshold(
#         # ammo_img,                                  
#         # maxValue=255,                              
#         # adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
#         # thresholdType=cv2.THRESH_BINARY,           
#         # blockSize=11,                              
#         # C=1)
#     ammo_img = np.                                       
#     cv2.imshow("ammo", ammo_img)
#     cv2.waitKey(0)

# For Getting Data
#     file = r'C:/Users/CafuuChino/Desktop/Apex/scr'

#     for root, dirs, files in os.walk(file):
#         if root != file:
#                 break
#         for file in files:
#                 path = os.path.join(root, file)
#                 print(file, end = " ")
#                 img = cv2.imread(path)
#                 stat_weapon_image(img)
#     cv2.destroyAllWindows()
