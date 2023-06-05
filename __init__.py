from pynput import keyboard
from screen_recorder import ScreenRecorder
from weapon_detector import WeaponDetector


def on_press(key):
    if key == keyboard.Key.delete:
        screen_recorder.stop()
        return


if __name__ == '__main__':
    weapon_manager = WeaponDetector()
    screen_recorder = ScreenRecorder()
    screen_recorder.register("weapon_manager", weapon_manager)
    keyboard.Listener(on_press=on_press).start()
    print("Press delete to stop")
    screen_recorder.start()
