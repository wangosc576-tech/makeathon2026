import subprocess
import time
import numpy as np
import os


def capture_frame():
    clean_env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("PYTHONPATH", "VIRTUAL_ENV", "PATH")
    }
    clean_env["PATH"] = "/usr/bin:/bin"

    result = subprocess.run(
        ["python3", "camera.py"], capture_output=True, env=clean_env
    )
    if result.returncode != 0:
        print("Camera error:", result.stderr.decode())
        return None

    # first 12 bytes = 3 int32s = shape (height, width, channels)
    shape = np.frombuffer(result.stdout[:12], dtype=np.int32)
    frame = np.frombuffer(result.stdout[12:], dtype=np.uint8).reshape(shape)
    return frame


def capture_picture(output_path="image.jpg"):
    clean_env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("PYTHONPATH", "VIRTUAL_ENV", "PATH")
    }
    clean_env["PATH"] = "/usr/bin:/bin"

    subprocess.run(["python3", "camera.py", "--save", output_path], env=clean_env)


if __name__ == "__main__":
    start_time = time.time()
    result = capture_frame()
    print(f"Loading a frame array took {time.time() - start_time}")
    start_time = time.time()
    capture_picture()
    print(f"Loading a frame array took {time.time() - start_time}")
