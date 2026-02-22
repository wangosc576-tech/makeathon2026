# ══════════════════════════════════════════════════════════════
#  ir_sensor.py  –  IR sensor that toggles the flashlight
#  To test standalone: python ir_sensor.py
# ══════════════════════════════════════════════════════════════

import gpio_manager  # ensures GPIO.setmode is called first
import RPi.GPIO as GPIO
import time
from config import IR_SENSOR_PIN, IR_COOLDOWN

GPIO.setup(IR_SENSOR_PIN, GPIO.IN)

_last_trigger = 0
_was_detected = False

def detected():
    """
    Returns True if the IR sensor currently sees something.
    Most IR sensors output LOW when triggered – flip to GPIO.HIGH
    if yours behaves the opposite way.
    """
    return GPIO.input(IR_SENSOR_PIN) == GPIO.LOW

def check_toggle(toggle_fn):
    """
    Call this in a loop. Fires toggle_fn() once per detection event
    (rising edge only) with a cooldown to prevent rapid re-triggering.
    """
    global _last_trigger, _was_detected

    now               = time.time()
    currently         = detected()
    rising_edge       = currently and not _was_detected
    cooldown_elapsed  = now - _last_trigger > IR_COOLDOWN

    if rising_edge and cooldown_elapsed:
        _last_trigger = now
        toggle_fn()

    _was_detected = currently

# ── Standalone test ───────────────────────────────────────────
if __name__ == "__main__":
    print("IR sensor test – wave your hand. Ctrl+C to stop.")
    try:
        while True:
            state = "DETECTED" if detected() else "clear"
            print(f"\r IR: {state}          ", end="", flush=True)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nDone.")
        gpio_manager.cleanup()
