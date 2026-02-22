# ══════════════════════════════════════════════════════════════
#  touch_sensor.py  –  single and double tap detection
#  To test standalone: python touch_sensor.py
# ══════════════════════════════════════════════════════════════

import gpio_manager  # ensures GPIO.setmode is called first
import RPi.GPIO as GPIO
import time
from config import TOUCH_PIN, DOUBLE_TAP_WINDOW

GPIO.setup(TOUCH_PIN, GPIO.IN)

_last_tap_time   = 0.0
_was_touched     = False
_pending_single  = False  # True when we have one tap and are waiting for a possible second

def is_touched():
    """
    Returns True if the touch sensor is active.
    Most touch sensors output HIGH when touched – flip to GPIO.LOW
    if yours behaves the opposite way.
    """
    return GPIO.input(TOUCH_PIN) == GPIO.HIGH

def check(on_single_tap, on_double_tap):
    """
    Call this in a loop. Detects single and double taps cleanly.

    Logic:
    - On the first tap (rising edge), record the time and mark a pending single tap.
    - If a second tap (rising edge) arrives within DOUBLE_TAP_WINDOW, fire double tap
      and clear the pending single.
    - If DOUBLE_TAP_WINDOW expires with no second tap, fire single tap.

    This means single tap always waits DOUBLE_TAP_WINDOW before firing,
    but double tap fires immediately on the second touch.
    """
    global _last_tap_time, _was_touched, _pending_single

    now           = time.time()
    currently     = is_touched()
    rising_edge   = currently and not _was_touched

    if rising_edge:
        if _pending_single and (now - _last_tap_time) < DOUBLE_TAP_WINDOW:
            # Second tap within window → double tap
            print("[TOUCH] Double tap!")
            on_double_tap()
            _pending_single = False
            _last_tap_time  = 0.0
        else:
            # First tap – start the window
            _last_tap_time  = now
            _pending_single = True

    # If a single tap is pending and the window has expired with no second tap
    if _pending_single and (now - _last_tap_time) > DOUBLE_TAP_WINDOW:
        print("[TOUCH] Single tap!")
        on_single_tap()
        _pending_single = False
        _last_tap_time  = 0.0

    _was_touched = currently

# ── Standalone test ───────────────────────────────────────────
if __name__ == "__main__":
    print("Touch sensor test – tap for single, double tap for double. Ctrl+C to stop.")
    try:
        while True:
            check(
                on_single_tap = lambda: print("→ Single tap fired"),
                on_double_tap = lambda: print("→ Double tap fired"),
            )
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nDone.")
        gpio_manager.cleanup()
