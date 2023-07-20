from pynput.keyboard import Key, Listener

from device_factory import MouseEmulator
from image_debugger import ImageDebugger
from image_producer import ImageProducer
from recoil_suppressor import RecoilSuppressor
from weapon_detector import WeaponDetector


def on_press(key):
    if key == Key.delete:
        image_producer.stop()
        return


if __name__ == '__main__':
    mouse_emulator = MouseEmulator()
    image_debugger = ImageDebugger("Weapon Detector")
    image_producer = ImageProducer()
    recoil_suppressor = RecoilSuppressor()
    weapon_detector = WeaponDetector()

    image_producer.register(weapon_detector)
    weapon_detector.set_debugger(image_debugger)
    weapon_detector.register(recoil_suppressor)

    Listener(on_press=on_press).start()

    print("Press delete to stop")

    image_producer.start()
