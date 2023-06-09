from pynput import keyboard

from image_debugger import ImageDebugger
from screen_recorder import ScreenRecorder
from weapon_detector import WeaponDetector


def on_press(key):
    if key == keyboard.Key.delete:
        screen_recorder.stop()
        return


if __name__ == '__main__':
    image_debugger = ImageDebugger("Weapon Detector")
    screen_recorder = ScreenRecorder()
    weapon_detector = WeaponDetector()

    screen_recorder.register("weapon_manager", weapon_detector)
    weapon_detector.set_debugger(image_debugger)

    keyboard.Listener(on_press=on_press).start()

    print("Press delete to stop")

    screen_recorder.start()
