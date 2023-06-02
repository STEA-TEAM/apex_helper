from screen_recorder import ScreenRecorder
from weapon_detector import WeaponDetector

if __name__ == '__main__':
    weapon_manager = WeaponDetector()
    screen_recorder = ScreenRecorder()
    screen_recorder.register("weapon_manager", weapon_manager)
    screen_recorder.start()
