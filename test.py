from datetime import datetime

import cv2
from pynput.keyboard import Key, Listener
from ultralytics import YOLO

import bettercam
import math
import NDIlib
import numpy as np
import sys
import torch
import intel_extension_for_pytorch as ipex

from structures import ImageEditor
from utils import image_in_rectangle

is_running = True


def on_press(key):
    if key == Key.delete:
        global is_running
        is_running = False


def main():
    if not NDIlib.initialize():
        return 0

    model = YOLO("apex_8s.pt").to(torch.device("xpu"))
    timestamps = [datetime.now().timestamp()]
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
        timestamps.append(datetime.now().timestamp())
        if timestamps.__len__() > 5:
            timestamps.pop(0)
        fps_text = f"Fps: {1 / np.average(np.diff(timestamps))}"
        payload = camera.get_latest_frame()
        offset = (math.floor((payload.shape[1] - payload.shape[0]) / 2), 0)
        cropped_image = image_in_rectangle(
            payload,
            (
                offset,
                (
                    math.floor((payload.shape[1] + payload.shape[0]) / 2),
                    payload.shape[0],
                ),
            ),
        )
        image_editor = ImageEditor(cv2.cvtColor(payload, cv2.COLOR_BGR2BGRA))
        image_editor.add_rectangle(
            (
                offset,
                (
                    math.floor((payload.shape[1] + payload.shape[0]) / 2),
                    payload.shape[0],
                ),
            ),
            (255, 255, 255, 127)
        )
        for result in model.predict(source=cv2.cvtColor(cropped_image, cv2.COLOR_BGRA2BGR), verbose=False):
            for box in result.boxes.cpu():
                dimension = np.floor(box.xyxy[0].numpy()).astype(int)
                class_name = model.names[int(box.cls)]
                image_editor.add_rectangle(
                    (
                        (offset[0] + dimension[0], offset[1] + dimension[1]),
                        (offset[0] + dimension[2], offset[1] + dimension[3]),
                    ),
                    class_name == "allies" and (0, 255, 0, 255) or (0, 0, 255, 255),
                )
                image_editor.add_text(
                    class_name,
                    (offset[0] + dimension[0], offset[1] + dimension[1] - 10),
                    1.0,
                    class_name == "allies" and (0, 255, 0, 255) or (0, 0, 255, 255),
                )
        image_editor.add_text(fps_text, (5, 15), 0.5, (127, 127, 127, 255), 5)
        image_editor.add_text(fps_text, (5, 15), 0.5, (255, 255, 0, 255), 1)
        data = image_editor.image
        video_frame.data = data
        NDIlib.send_send_video_v2(ndi_send, video_frame)

    camera.stop()
    NDIlib.send_destroy(ndi_send)
    NDIlib.destroy()

    return 0


if __name__ == "__main__":
    Listener(on_press=on_press).start()
    sys.exit(main())
