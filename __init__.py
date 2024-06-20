from components import (
    EmulateAdapter,
    EnemyTracker,
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
    emulate_adapter = EmulateAdapter()
    enemy_tracker = EnemyTracker()
    image_producer = ImageProducer()
    input_handler = InputHandler()
    player_detector = PlayerDetector("apex_8n.onnx")
    # recoil_suppressor = RecoilSuppressor()
    # weapon_detector = WeaponDetector()
    ws_server = WsServer()

    enemy_tracker.add_consumer(emulate_adapter)
    # enemy_tracker.ws_server = ws_server

    image_producer.add_tasker(player_detector)
    # image_producer.add_tasker(weapon_detector)

    input_handler.add_tasker(enemy_tracker)
    # input_handler.add_tasker(recoil_suppressor)

    player_detector.add_subscriber(enemy_tracker)
    # player_detector.ws_server = ws_server

    # recoil_suppressor.add_consumer(emulate_adapter)

    # weapon_detector.add_subscriber(recoil_suppressor)

    listener.start()
    print("Press delete to stop")
    thread_manager.start()
