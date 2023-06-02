from screen_recorder import ScreenRecorder
from weapon_manager import WeaponManager

if __name__ == '__main__':
    weapon_manager = WeaponManager()
    screen_recorder = ScreenRecorder()
    screen_recorder.register("weapon_manager", weapon_manager)
    screen_recorder.start()
