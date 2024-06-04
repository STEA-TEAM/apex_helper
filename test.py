import bettercam
import cv2

if __name__ == "__main__":
    camera = bettercam.create(output_color="BGR")
    camera.start(target_fps=240)
    while camera.is_capturing:
        frame = camera.get_latest_frame()
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    camera.stop()
