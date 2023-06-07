import cv2

from weapon_detector import WeaponDetector

if __name__ == '__main__':
    weapon_detector_4k = WeaponDetector("4k", 1.0, (3840, 2160))
    weapon_detector_4k(cv2.imread("C:/Users/particleg/Desktop/Apex/3840/flatline.bmp"))
    weapon_detector_2k = WeaponDetector("2k", 3840 / 2560)
    weapon_detector_2k(cv2.imread("C:/Users/particleg/Desktop/Apex/2560/flatline.bmp"))
    cv2.waitKey(0)
