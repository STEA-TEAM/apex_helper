from pynput.keyboard import Key, Listener

import bettercam
import NDIlib
import sys

is_running = True


def on_press(key):
    if key == Key.delete:
        global is_running
        is_running = False


def main():
    if not NDIlib.initialize():
        return 0

    send_settings = NDIlib.SendCreate()
    send_settings.ndi_name = "apex_helper"
    ndi_send = NDIlib.send_create(send_settings)
    video_frame = NDIlib.VideoFrameV2(
        FourCC=NDIlib.FOURCC_VIDEO_TYPE_BGRA,
        frame_rate_D=1000,
        frame_rate_N=60000,
    )
    camera = bettercam.create(output_color="BGRA")
    camera.start(target_fps=240)

    while is_running:
        frame = camera.get_latest_frame()
        video_frame.data = frame
        NDIlib.send_send_video_v2(ndi_send, video_frame)

    camera.stop()
    NDIlib.send_destroy(ndi_send)
    NDIlib.destroy()

    return 0


if __name__ == "__main__":
    Listener(on_press=on_press).start()
    sys.exit(main())
