import bettercam
from image_debugger import ImageDebugger

if __name__ == "__main__":
    camera = bettercam.create(output_color="BGR")
    camera.start(target_fps=240)
    image_debugger = ImageDebugger()
    for i in range(500):
        frame = camera.get_latest_frame()
        image_debugger.set_image(frame)
        # image_debugger.show()
    camera.stop()
