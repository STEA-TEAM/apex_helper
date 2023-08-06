from multiprocessing import Event
from pynput.keyboard import Key, Listener

from image_debugger import ImageDebugger
from image_producer import ImageProducer
from input_handler import InputHandler
from recoil_suppressor import RecoilSuppressor
from weapon_detector import WeaponDetector

terminate_event: Event = Event()


def on_press(key):
    if key == Key.delete:
        image_producer.terminate()
        input_handler.terminate()
        terminate_event.set()
        return


if __name__ == "__main__":
    image_producer = ImageProducer()
    input_handler = InputHandler()
    recoil_suppressor = RecoilSuppressor()
    weapon_broadcaster = WeaponDetector()

    image_producer.add_tasker(weapon_broadcaster)
    weapon_broadcaster.set_debugger(ImageDebugger("Weapon Detector"))
    weapon_broadcaster.add_subscriber(recoil_suppressor)
    input_handler.add_tasker(recoil_suppressor)

    Listener(on_press=on_press).start()

    print("Press delete to stop")

    image_producer.start()
    input_handler.start()

    while not terminate_event.is_set():
        pass
