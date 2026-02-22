import subprocess
import threading
import time
_capture_thread = None
_last_capture = 0

def capture_picture():
    global _capture_thread, _last_capture
    now = time.time()
    if now - _last_capture < 5:
        return
    if _capture_thread is not None and _capture_thread.is_alive():
        return
    _last_capture = now
    _capture_thread = threading.Thread(
        target=lambda: subprocess.run(["bash", "/home/makeathon/real/makeathon2026/SensorVersion/capture.sh"]),
        daemon=True
    )
    _capture_thread.start()
