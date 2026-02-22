# ══════════════════════════════════════════════════════════════
#  camera.py  –  takes and saves photos using the Pi Camera
#  To test standalone: python camera.py
# ══════════════════════════════════════════════════════════════

from picamera2 import Picamera2
from datetime import datetime
import os
import time
from config import PHOTO_SAVE_DIR

_cam = None

def init():
    """
    Initialise the Pi Camera. Call once at startup.
    Also creates the photo save directory if it doesn't exist.
    """
    global _cam
    os.makedirs(PHOTO_SAVE_DIR, exist_ok=True)  # only runs when explicitly initialised
    _cam = Picamera2()
    _cam.configure(_cam.create_still_configuration())
    _cam.start()
    time.sleep(0.5)  # let sensor stabilise
    print(f"[CAMERA] Ready. Saving photos to: {PHOTO_SAVE_DIR}")

def take_photo():
    """
    Capture a photo and save it with a timestamp filename.
    Returns the file path, or None if the camera isn't initialised.
    """
    if _cam is None:
        print("[CAMERA] Not initialised – call camera.init() first.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath  = os.path.join(PHOTO_SAVE_DIR, f"photo_{timestamp}.jpg")
    _cam.capture_file(filepath)
    print(f"[CAMERA] Photo saved → {filepath}")
    return filepath

def cleanup():
    global _cam
    if _cam is not None:
        _cam.stop()
        _cam = None

# ── Standalone test ───────────────────────────────────────────
if __name__ == "__main__":
    init()
    print("Taking a test photo in 3 seconds...")
    time.sleep(3)
    path = take_photo()
    print(f"Saved to: {path}")
    cleanup()
