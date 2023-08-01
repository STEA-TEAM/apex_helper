import cv2

from image_debugger import ImageDebugger
from weapon_detector import WeaponDetector

if __name__ == '__main__':
    image_debugger_2k = ImageDebugger("2K")
    image_debugger_4k = ImageDebugger("4K")
    weapon_detector_2k = WeaponDetector((2560, 1600))
    weapon_detector_4k = WeaponDetector((3840, 2160))

    weapon_detector_2k.set_debugger(image_debugger_2k)
    weapon_detector_4k.set_debugger(image_debugger_4k)

    cv2.waitKey(0)
