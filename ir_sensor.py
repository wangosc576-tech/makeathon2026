# ══════════════════════════════════════════════════════════════
#  ir_sensor.py  –  IR sensor wake trigger
#  To test standalone: python ir_sensor.py
# ══════════════════════════════════════════════════════════════

import RPi.GPIO as GPIO
from config import IR_SENSOR_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)

def detected():
    """
    Returns True if the IR sensor is detecting something nearby.
    Most IR obstacle sensors output LOW when triggered, HIGH when clear.
    Flip to GPIO.HIGH if yours behaves the opposite way.
    """
    return GPIO.input(IR_SENSOR_PIN) == GPIO.LOW

def cleanup():
    GPIO.cleanup()

# ── Standalone test ───────────────────────────────────────────
if __name__ == "__main__":
    import time
    print("IR sensor test – wave your hand in front of it. Ctrl+C to stop.")
    try:
        while True:
            state = "DETECTED" if detected() else "clear"
            print(f"\r IR: {state}          ", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nDone.")
        cleanup()
