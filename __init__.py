from components import (
    EmulateAdapter,
    ImageProducer,
    InputHandler,
    PlayerDetector,
    RecoilSuppressor,
    WeaponDetector,
)
from pynput.keyboard import Key, Listener
from components.websocket_server.websocket_server import WebsocketServer
from structures import thread_manager
from structures.ws_message.handshake_server_message import HandshakeServerMessage

websocket_server = WebsocketServer()


def on_press(key):
    if key == Key.delete:
        global listener
        thread_manager.terminate()
        listener.stop()
    elif key == Key.insert:
        global websocket_server
        websocket_server.broadcast(
            HandshakeServerMessage(
                {
                    "resolution": {"height": 1080, "width": 1920},
                    "fps": 60,
                    "name": "Apex Legends",
                }
            )
        )


listener = Listener(on_press=on_press)

if __name__ == "__main__":
    # emulate_adapter = EmulateAdapter()
    # image_producer = ImageProducer()
    # input_handler = InputHandler()
    # player_detector = PlayerDetector("apex_8s.pt")
    # recoil_suppressor = RecoilSuppressor()
    # weapon_detector = WeaponDetector()

    # image_producer.add_tasker(weapon_detector)
    # image_producer.add_tasker(player_detector)

    # input_handler.add_tasker(recoil_suppressor)

    # weapon_detector.add_subscriber(recoil_suppressor)

    # recoil_suppressor.add_consumer(emulate_adapter)

    listener.start()
    print("Press delete to stop")
    thread_manager.start()
