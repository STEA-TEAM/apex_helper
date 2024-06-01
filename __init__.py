from device_adapters import EmulateAdapter
from image_debugger import ImageDebugger
from image_producer import ScreenRecorder
from input_handler import InputHandler
from pynput.keyboard import Key, Listener

from player_detector import PlayerDetector
from recoil_suppressor import RecoilSuppressor
from structures import thread_manager
from weapon_detector import WeaponDetector


def on_press(key):
    if key == Key.delete:
        thread_manager.terminate()


if __name__ == "__main__":
    emulate_adapter = EmulateAdapter()
    screen_recorder = ScreenRecorder()
    input_handler = InputHandler()
    player_detector = PlayerDetector()
    recoil_suppressor = RecoilSuppressor()
    weapon_detector = WeaponDetector()

    (
        thread_manager.register(emulate_adapter)
        .register(screen_recorder)
        .register(input_handler)
    )

    screen_recorder.add_tasker(weapon_detector)
    screen_recorder.add_tasker(player_detector)

    weapon_detector.set_debugger(ImageDebugger("Weapon Detector"))
    weapon_detector.add_subscriber(recoil_suppressor)

    player_detector.set_debugger(ImageDebugger("Player Detector"))

    input_handler.add_tasker(recoil_suppressor)
    recoil_suppressor.add_consumer(emulate_adapter)

    Listener(on_press=on_press).start()

    print("Press delete to stop")

    thread_manager.start()
