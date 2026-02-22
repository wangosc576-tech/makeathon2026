# ══════════════════════════════════════════════════════════════
#  main.py  –  entry point, ties everything together
#  Run with: python main.py
# ══════════════════════════════════════════════════════════════

import time
import ir_sensor
import vision
from debouncer import GestureDebouncer
from gesture_map import GESTURE_MAP
from config import IR_COOLDOWN
from camera import Camera
import RPi.GPIO as GPIO


def main():
    print("=== Shoulder Companion ===")
    print("Mapped gestures:")
    for fingers, fn in GESTURE_MAP.items():
        print(f"  {fingers} finger(s) → {fn.__name__}")
    print("Waiting for IR trigger...\n")

    cam = Camera()
    debouncer = GestureDebouncer()
    last_ir_time = 0
    gesture_active = False
    active_label = "None"

    try:
        while True:
            # ── IR wake check ──────────────────────────────────
            if ir_sensor.detected():
                last_ir_time = time.time()
                gesture_active = True
            elif gesture_active:
                if time.time() - last_ir_time > IR_COOLDOWN:
                    gesture_active = False
                    debouncer.clear()
                    print("[IR] Hand gone – sleeping.")

            # ── Sleep mode ─────────────────────────────────────
            if not gesture_active:
                time.sleep(0.05)
                continue

            # ── Active mode: get gesture and trigger action ────
            finger_count = vision.get_gesture(cam)

            if finger_count is not None:
                confirmed = debouncer.update(finger_count)
                if confirmed is not None and confirmed in GESTURE_MAP:
                    # GESTURE_MAP[confirmed]() $ (Uncomment when fixed)
                    print(f"[GESTURE] {confirmed} finger(s)")
            else:
                debouncer.clear()

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        GPIO.cleanup()
        cam.stop()
        print("Cleaned up. Goodbye!")


if __name__ == "__main__":
    main()
