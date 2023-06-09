from pynput import keyboard

from image_debugger import ImageDebugger
from screen_recorder import ImageProducer
from weapon_detector import WeaponDetector


def on_press(key):
    if key == keyboard.Key.delete:
        image_producer.stop()
        return


if __name__ == '__main__':
    image_debugger = ImageDebugger("Weapon Detector")
    image_producer = ImageProducer()
    weapon_detector = WeaponDetector()

    image_producer.register(weapon_detector)
    weapon_detector.set_debugger(image_debugger)

    keyboard.Listener(on_press=on_press).start()

    print("Press delete to stop")

    image_producer.start()
