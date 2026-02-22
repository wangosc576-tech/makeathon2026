from picamera2 import Picamera2
from config import CAMERA_WIDTH, CAMERA_HEIGHT, JPG_QUALITY
from datetime import datetime
import time
import numpy as np
import sys


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

    def capture_frame(self):
        return self.cam.capture_array()

    def capture_picture(self, path=None):
        if path is None:
            path = datetime.now().strftime("photo_%Y%m%d_%H%M%S.jpg")
        self.cam.capture_file(path)
        return path

    def stop(self):
        self.cam.stop()


if __name__ == "__main__":
    cam = Camera()

    if "--save" in sys.argv:
        idx = sys.argv.index("--save")
        # use provided path or generate timestamped name
        path = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        saved = cam.capture_picture(path)
        print(f"Saved: {saved}", file=sys.stderr)
    else:
        # default: output raw frame bytes to stdout
        frame = cam.capture_frame()
        sys.stdout.buffer.write(np.array(frame.shape, dtype=np.int32).tobytes())
        sys.stdout.buffer.write(frame.tobytes())

    cam.stop()
