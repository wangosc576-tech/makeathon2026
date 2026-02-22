# ══════════════════════════════════════════════════════════════
#  flashlight.py  –  flashlight hardware control
#  To test standalone: python flashlight.py
# ══════════════════════════════════════════════════════════════

import gpio_manager  # ensures GPIO.setmode is called first
import RPi.GPIO as GPIO
from config import FLASHLIGHT_PIN, PWM_FREQ

GPIO.setup(FLASHLIGHT_PIN, GPIO.OUT)

_pwm   = GPIO.PWM(FLASHLIGHT_PIN, PWM_FREQ)
_pwm.start(0)
_is_on = False

def on():
    global _is_on
    _pwm.ChangeDutyCycle(100)
    _is_on = True
    print("[FLASHLIGHT] ON")

def off():
    global _is_on
    _pwm.ChangeDutyCycle(0)
    _is_on = False
    print("[FLASHLIGHT] OFF")

def toggle():
    """Turn off if on, turn on if off."""
    off() if _is_on else on()

def cleanup():
    """Stop PWM cleanly. Does NOT call GPIO.cleanup() – gpio_manager handles that."""
    off()
    _pwm.stop()

# ── Standalone test ───────────────────────────────────────────
if __name__ == "__main__":
    import time
    print("Flashlight test – ON for 2s then OFF.")
    on()
    time.sleep(2)
    off()
    cleanup()
    gpio_manager.cleanup()
