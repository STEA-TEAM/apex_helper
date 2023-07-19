from pynput.keyboard import Controller as KeyController, Key, Listener
from pynput.mouse import Controller as MouseController, Button

from device_factory import MouseEmulator, MouseEventFlag
from image_debugger import ImageDebugger
from screen_recorder import ImageProducer
from weapon_detector import WeaponDetector

key_controller = KeyController()
mouse_controller = MouseController()

def on_press(key):
    if key == Key.f7:
        print("Try send key 4 to the game")
        key_controller.press('5')
        key_controller.release('5')
    if key == Key.f8:
        print("Try send mouse move to the game")

    if key == Key.delete:
        # image_producer.stop()
        mouse_emulator.stop()
        return


if __name__ == '__main__':
    # image_debugger = ImageDebugger("Weapon Detector")
    # image_producer = ImageProducer()
    # weapon_detector = WeaponDetector()
    #
    # image_producer.register(weapon_detector)
    # weapon_detector.set_debugger(image_debugger)
    #
    # Listener(on_press=on_press).start()
    #
    # print("Press delete to stop")
    #
    # image_producer.start()
    mouse_emulator = MouseEmulator()
    mouse_emulator.push_events([
        ([MouseEventFlag.Move, MouseEventFlag.LeftDown], (10, 0), 0, 0.1),
        ([MouseEventFlag.Move], (10, 0), 0, 0.1),
        ([MouseEventFlag.Move], (0, 10), 0, 0.1),
        ([MouseEventFlag.Move], (0, 10), 0, 0.1),
        ([MouseEventFlag.Move], (-10, 0), 0, 0.1),
        ([MouseEventFlag.Move], (-10, 0), 0, 0.1),
        ([MouseEventFlag.Move], (0, -10), 0, 0.1),
        ([MouseEventFlag.Move, MouseEventFlag.LeftUp], (0, -10), 0, 0.1),
    ])
    mouse_emulator.start()
