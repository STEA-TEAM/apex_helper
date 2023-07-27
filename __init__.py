from pynput.keyboard import Key, Listener

from device_adapters import EmulateAdapter
from image_debugger import ImageDebugger
from image_factory import ImageProducer
from recoil_suppressor import RecoilSuppressor
from weapon_factory import WeaponBroadcaster


def on_press(key):
    if key == Key.delete:
        image_producer.stop()
        return


if __name__ == '__main__':
    emulate_emulator = EmulateAdapter()
    image_debugger = ImageDebugger("Weapon Detector")
    image_producer = ImageProducer()
    recoil_suppressor = RecoilSuppressor()
    weapon_broadcaster = WeaponBroadcaster()

    image_producer.register(weapon_broadcaster)
    weapon_broadcaster.set_debugger(image_debugger)
    weapon_broadcaster.register(recoil_suppressor)

    Listener(on_press=on_press).start()

    print("Press delete to stop")

    image_producer.start()
