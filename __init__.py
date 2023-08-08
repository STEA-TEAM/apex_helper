from device_adapters import EmulateAdapter
from image_debugger import ImageDebugger
from image_producer import ImageProducer
from input_handler import InputHandler
from pynput.keyboard import Key, Listener
from recoil_suppressor import RecoilSuppressor
from weapon_detector import WeaponDetector


def on_press(key):
    if key == Key.delete:
        emulate_adapter.terminate()
        image_producer.terminate()
        input_handler.terminate()
        return


if __name__ == "__main__":
    emulate_adapter = EmulateAdapter()
    image_producer = ImageProducer()
    input_handler = InputHandler()
    recoil_suppressor = RecoilSuppressor()
    weapon_broadcaster = WeaponDetector()

    image_producer.add_tasker(weapon_broadcaster)
    weapon_broadcaster.set_debugger(ImageDebugger("Weapon Detector"))
    weapon_broadcaster.add_subscriber(recoil_suppressor)
    input_handler.add_tasker(recoil_suppressor)
    recoil_suppressor.add_consumer(emulate_adapter)
    Listener(on_press=on_press).start()

    print("Press delete to stop")

    emulate_adapter.start()
    image_producer.start()
    input_handler.start()
