import subprocess
import time
import threading
import datetime
import numpy as np
import os

_capture_thread = None  # track thread directly instead of a boolean flag

def _clean_env():
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("PYTHONPATH", "VIRTUAL_ENV", "PATH")
    }
    env["PATH"] = "/usr/bin:/bin"
    return env

def capture_frame():
    result = subprocess.run(
        ["python3", "camera.py"], capture_output=True, env=_clean_env()
    )
    if result.returncode != 0:
        print("Camera error:", result.stderr.decode())
        return None
    shape = np.frombuffer(result.stdout[:12], dtype=np.int32)
    frame = np.frombuffer(result.stdout[12:], dtype=np.uint8).reshape(shape)
    return frame

def _do_capture(output_path):
    try:
        subprocess.run(
            ["python3", "camera.py", "--save", output_path],
            env=_clean_env(),
            capture_output=True,  # prevents stdout blocking the thread
            timeout=30
        )
        print(f"[CAM] Saved {output_path}")
    except subprocess.TimeoutExpired:
        print("[CAM] Timed out.")
    except Exception as e:
        print(f"[CAM] Error: {e}")

def capture_picture():
    global _capture_thread
    if _capture_thread is not None and _capture_thread.is_alive():
        print("[CAM] Already capturing, skipping.")
        return
    output_path = datetime.datetime.now().strftime("photo_%Y%m%d_%H%M%S.jpg")
    print(f"[CAM] Capturing to {output_path}")
    _capture_thread = threading.Thread(target=_do_capture, args=(output_path,), daemon=True)
    _capture_thread.start()

if __name__ == "__main__":
    start_time = time.time()
    result = capture_frame()
    print(f"Frame capture took {time.time() - start_time:.2f}s")

    start_time = time.time()
    capture_picture()
    time.sleep(5)  # wait for background thread in test
    print(f"Picture capture took {time.time() - start_time:.2f}s")
import subprocess
import time
import threading
import datetime
import numpy as np
import os

_capture_thread = None  # track thread directly instead of a boolean flag

def _clean_env():
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("PYTHONPATH", "VIRTUAL_ENV", "PATH")
    }
    env["PATH"] = "/usr/bin:/bin"
    return env

def capture_frame():
    result = subprocess.run(
        ["python3", "camera.py"], capture_output=True, env=_clean_env()
    )
    if result.returncode != 0:
        print("Camera error:", result.stderr.decode())
        return None
    shape = np.frombuffer(result.stdout[:12], dtype=np.int32)
    frame = np.frombuffer(result.stdout[12:], dtype=np.uint8).reshape(shape)
    return frame

def _do_capture(output_path):
    try:
        subprocess.run(
            ["python3", "camera.py", "--save", output_path],
            env=_clean_env(),
            capture_output=True,  # prevents stdout blocking the thread
            timeout=10
        )
        print(f"[CAM] Saved {output_path}")
    except subprocess.TimeoutExpired:
        print("[CAM] Timed out.")
    except Exception as e:
        print(f"[CAM] Error: {e}")

def capture_picture():
    global _capture_thread
    if _capture_thread is not None and _capture_thread.is_alive():
        print("[CAM] Already capturing, skipping.")
        return
    output_path = datetime.datetime.now().strftime("photo_%Y%m%d_%H%M%S.jpg")
    print(f"[CAM] Capturing to {output_path}")
    _capture_thread = threading.Thread(target=_do_capture, args=(output_path,), daemon=True)
    _capture_thread.start()

if __name__ == "__main__":
    start_time = time.time()
    result = capture_frame()
    print(f"Frame capture took {time.time() - start_time:.2f}s")

    start_time = time.time()
    capture_picture()
    time.sleep(5)  # wait for background thread in test
    print(f"Picture capture took {time.time() - start_time:.2f}s")

