# ══════════════════════════════════════════════════════════════
#  flashlight.py  –  all flashlight hardware control
#  To test standalone: python flashlight.py
# ══════════════════════════════════════════════════════════════

import RPi.GPIO as GPIO
from config import FLASHLIGHT_PIN, PWM_FREQ

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLASHLIGHT_PIN, GPIO.OUT)

_pwm = GPIO.PWM(FLASHLIGHT_PIN, PWM_FREQ)
_pwm.start(0)

def set_brightness(brightness):
    """Set flashlight brightness 0–100."""
    _pwm.ChangeDutyCycle(max(0, min(100, brightness)))

def on():
    """Turn flashlight on at full brightness."""
    print("[FLASHLIGHT] ON")
    set_brightness(100)

def off():
    """Turn flashlight off."""
    print("[FLASHLIGHT] OFF")
    set_brightness(0)

def cleanup():
    """Call this on program exit to release GPIO."""
    off()
    _pwm.stop()
    GPIO.cleanup()

# ── Standalone test ───────────────────────────────────────────
if __name__ == "__main__":
    import time
    print("Flashlight test – turning on for 3 seconds...")
    on()
    time.sleep(3)
    off()
    cleanup()
    print("Done.")
