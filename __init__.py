from pynput.keyboard import Key, Listener

from image_debugger import ImageDebugger
from image_producer import ImageProducer
from input_handler import InputHandler
from recoil_suppressor import RecoilSuppressor
from weapon_detector import WeaponDetector


def on_press(key):
    if key == Key.delete:
        image_producer.terminate()
        input_handler.terminate()
        return


if __name__ == "__main__":
    image_producer = ImageProducer()
    input_handler = InputHandler()
    recoil_suppressor = RecoilSuppressor()
    weapon_broadcaster = WeaponDetector()

    image_producer.register(weapon_broadcaster)
    weapon_broadcaster.set_debugger(ImageDebugger("Weapon Detector"))
    weapon_broadcaster.register(recoil_suppressor)
    input_handler.register(recoil_suppressor)

    Listener(on_press=on_press).start()

    print("Press delete to stop")

    image_producer.start()
    input_handler.start()
