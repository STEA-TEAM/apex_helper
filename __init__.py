from components import (
    EmulateAdapter,
    ImageProducer,
    InputHandler,
    PlayerDetector,
    RecoilSuppressor,
    WeaponDetector,
    WsServer
)
from pynput.keyboard import Key, Listener
from structures import thread_manager


def on_press(key):
    if key == Key.delete:
        global listener
        thread_manager.terminate()
        listener.stop()


listener = Listener(on_press=on_press)

if __name__ == "__main__":
    # emulate_adapter = EmulateAdapter()
    image_producer = ImageProducer()
    # input_handler = InputHandler()
    player_detector = PlayerDetector("apex_8s.pt")
    # recoil_suppressor = RecoilSuppressor()
    # weapon_detector = WeaponDetector()
    ws_server = WsServer()

    image_producer.add_tasker(player_detector)
    # image_producer.add_tasker(weapon_detector)

    # input_handler.add_tasker(recoil_suppressor)

    player_detector.ws_server = ws_server

    # weapon_detector.add_subscriber(recoil_suppressor)

    # recoil_suppressor.add_consumer(emulate_adapter)

    listener.start()
    print("Press delete to stop")
    thread_manager.start()
