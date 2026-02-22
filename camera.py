from picamera2 import Picamera2
from config import CAMERA_WIDTH, CAMERA_HEIGHT, JPG_QUALITY
import time


class Camera:
    def start(self):
        cam = Picamera2()
        config = cam.create_preview_configuration(
            main={"format": "RGB888", "size": (CAMERA_WIDTH, CAMERA_HEIGHT)}
        )
        cam.options["quality"] = JPG_QUALITY
        cam.configure(config)
        cam.start()
        time.sleep(0.5)  # let sensor stabilize
        return cam

    def __init__(self):
        self.cam = self.start()
        self.counter = 0

    def capture_frame(self):
        return self.cam.capture_array()

    def capture_picture(self):
        image_name = f"image_{self.counter}.jpg"
        self.cam.capture_file(image_name)
        self.counter += 1

    def stop(self):
        self.cam.stop()


if __name__ == "__main__":
    print("start camera")
    cam = Camera()
    cam.capture_picture()
    cam.stop()
    print("done")
