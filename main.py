import cv2
import numpy as np
import pyautogui
import time

import os

from datetime import datetime


class WeaponType(Enum):
    Unknown = 0
    Legendary = 1
    Energy = 2
    Heavy = 3
    Light = 4
    Shotgun = 5
    Sniper = 6


weapon_identities = {
    "r99": ((159, 47, 1), (290, 53, 0), (381, 56, 1)),
    "r301": ((146, 32, 1), (306, 47, 0), (377, 48, 1)),
    "re45": ((204, 42, 1), (272, 54, 0), (316, 101, 1)),
    "p2020": ((201, 31, 1), (256, 56, 0), (295, 102, 1)),
    "g7": ((138, 42, 1), (310, 54, 0), (398, 72, 1)),
    "flatline": ((132, 43, 1), (261, 52, 0), (322, 79, 1)),
    "prowler": ((211, 73, 1), (263, 61, 0), (338, 45, 1)),
    "hemlok": ((205, 59, 1), (288, 63, 0), (369, 64, 1)),
    "rampage": ((111, 44, 1), (284, 60, 0), (395, 58, 1)),
    "wingman": ((197, 61, 1), (282, 62, 0), (308, 94, 1)),
    "lstar": ((151, 81, 1), (273, 72, 0), (326, 30, 1)),
    "devotion": ((392, 34, 1), (316, 52, 0), (114, 36, 1)),
    "volt": ((280, 54, 0), (162, 44, 1), (352, 34, 1)),
    "havoc": ((304, 84, 1), (308, 62, 0), (266, 16, 1)),
    "spitfire": ((378, 36, 1), (296, 70, 1), (282, 16, 1)),
    "alternator": ((222, 50, 1), (276, 52, 1), (284, 48, 0)),
    "car": ((202, 32, 1), (164, 38, 1), (202, 34, 1)),
    "p3030": ((236, 42, 1), (396, 54, 0), (344, 68, 0)),
}

weapon_types = {1: WeaponType.Unknown, 2: WeaponType.Unknown}


def get_scale(_screen_size: pyautogui.Size):
    original_screen_width = 3840
    return _screen_size[0] / original_screen_width


def get_weapon_area(_screen_size: pyautogui.Size):
    scale = get_scale(_screen_size)
    area_width = round(731 * scale)
    area_height = round(207 * scale)
    margin_bottom = round(45 * scale)
    margin_right = round(101 * scale)
    return {
        "x": _screen_size[0] - area_width - margin_right,
        "y": _screen_size[1] - area_height - margin_bottom,
        "width": area_width,
        "height": area_height
    }


def get_weapon_points(_screen_size: pyautogui.Size):
    scale = get_scale(_screen_size)
    weapon_area = get_weapon_area(_screen_size)

    weapon_1_offset = (round(35 * scale), round(173 * scale))
    weapon_2_offset = (round(637 * scale), round(170 * scale))
    return (int(weapon_area["x"] + weapon_1_offset[0]), int(weapon_area["y"] + weapon_1_offset[1])), (
        int(weapon_area["x"] + weapon_2_offset[0]), int(weapon_area["y"] + weapon_2_offset[1]))


def get_weapon_type(color: (int, int, int)):
    if color == (178, 1, 55):
        return WeaponType.Legendary
    elif color == (90, 110, 40):
        return WeaponType.Energy
    elif color == (56, 107, 89):
        return WeaponType.Heavy
    elif color == (125, 84, 45):
        return WeaponType.Light
    elif color == (107, 32, 7):
        return WeaponType.Shotgun
    elif color == (75, 64, 143):
        return WeaponType.Sniper
    else:
        return WeaponType.Unknown


def get_weapon_identity(_screen_size: pyautogui.Size, _screenshot: ScreenShot):
    scale = get_scale(_screen_size)
    weapon_area = get_weapon_area(_screen_size)

    gray = cv2.cvtColor(np.array(_screenshot), cv2.COLOR_BGR2GRAY)
    gray = gray.transpose()
    # print(gray.shape)

    for weapon in weapon_identities:
        _weapon_identity = weapon_identities[weapon]
        if gray[
            int(weapon_area["x"] + round(_weapon_identity[0][0] * scale)), int(
                weapon_area["y"] + round(_weapon_identity[0][1] * scale))] >= _weapon_identity[0][2] * 255 and gray[
            int(weapon_area["x"] + round(_weapon_identity[1][0] * scale)), int(
                weapon_area["y"] + round(_weapon_identity[1][1] * scale))] >= _weapon_identity[1][2] * 255 and gray[
            int(weapon_area["x"] + round(_weapon_identity[2][0] * scale)), int(
                weapon_area["y"] + round(_weapon_identity[2][1] * scale))] >= _weapon_identity[2][2] * 255:
            return weapon
    return None


# Get the screen size
screen_size = pyautogui.size()
print(f"Screen size: {screen_size}")

while True:
    with mss() as sct:
        # Capture the screen
        screenshot = sct.grab({
            "top": 0,
            "left": 0,
            "width": screen_size[0],
            "height": screen_size[1]
        })

    # Get the weapon points
    weapon_points = get_weapon_points(screen_size)

    current_weapon_types = {
        1: get_weapon_type(screenshot.pixel(weapon_points[0][0], weapon_points[0][1])),
        2: get_weapon_type(screenshot.pixel(weapon_points[1][0], weapon_points[1][1]))
    }
    if current_weapon_types[1] != weapon_types[1]:
        weapon_types[1] = current_weapon_types[1]
        if weapon_types[1] is not WeaponType.Unknown:
            print(f"Weapon 1 active: {weapon_types[1]}")

    if current_weapon_types[2] != weapon_types[2]:
        weapon_types[2] = current_weapon_types[2]
        if weapon_types[2] is not WeaponType.Unknown:
            print(f"Weapon 2 active: {weapon_types[2]}")

    weapon_identity = get_weapon_identity(screen_size, screenshot)
    if weapon_identity is not None:
        print(f"Weapon identity: {weapon_identity}")

    # Display the frame
    # cv2.imshow("Screen", np.array(screenshot))

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the VideoWriter object and destroy the window
cv2.destroyAllWindows()
