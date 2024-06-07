from pynput.keyboard import Key, Listener

from components import (
    EmulateAdapter,
    ImageProducer,
    InputHandler,
    PlayerDetector,
    RecoilSuppressor,
    WeaponDetector
)
from structures import thread_manager


def on_press(key):
    if key == Key.delete:
        thread_manager.terminate()


if __name__ == "__main__":
    emulate_adapter = EmulateAdapter()
    image_producer = ImageProducer()
    input_handler = InputHandler()
    player_detector = PlayerDetector("apex_8s.pt")
    recoil_suppressor = RecoilSuppressor()
    weapon_detector = WeaponDetector()

    image_producer.add_tasker(weapon_detector)
    image_producer.add_tasker(player_detector)

    input_handler.add_tasker(recoil_suppressor)

    weapon_detector.add_subscriber(recoil_suppressor)

    recoil_suppressor.add_consumer(emulate_adapter)

    Listener(on_press=on_press).start()
    print("Press delete to stop")
    thread_manager.start()
