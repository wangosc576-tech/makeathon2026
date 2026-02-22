# ══════════════════════════════════════════════════════════════
#  buzzer.py  –  non-blocking buzzer control
#  To test standalone: python buzzer.py
#
#  FIX: beep() now runs in a background thread so it never
#  blocks the main loop while buzzing.
# ══════════════════════════════════════════════════════════════

import gpio_manager  # ensures GPIO.setmode is called first
import RPi.GPIO as GPIO
import time
import threading
from config import BUZZER_PIN, BUZZER_DURATION

GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

def _do_beep(duration):
    """Internal: runs in a background thread to avoid blocking."""
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def _do_double_beep():
    """Internal: two short beeps in a background thread."""
    _do_beep(0.15)
    time.sleep(0.1)
    _do_beep(0.15)

def beep(duration=BUZZER_DURATION):
    """Beep the buzzer without blocking the main loop."""
    print("[BUZZER] Beep!")
    threading.Thread(target=_do_beep, args=(duration,), daemon=True).start()

def double_beep():
    """Two short beeps without blocking the main loop."""
    print("[BUZZER] Double beep!")
    threading.Thread(target=_do_double_beep, daemon=True).start()

def cleanup():
    """Ensure buzzer is off on exit. gpio_manager handles GPIO.cleanup()."""
    GPIO.output(BUZZER_PIN, GPIO.LOW)

# ── Standalone test ───────────────────────────────────────────
if __name__ == "__main__":
    print("Buzzer test – single beep then double beep.")
    beep()
    time.sleep(1)
    double_beep()
    time.sleep(1)  # wait for threads to finish before cleanup
    cleanup()
    gpio_manager.cleanup()
