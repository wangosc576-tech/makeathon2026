# ══════════════════════════════════════════════════════════════
#  gpio_manager.py  –  GPIO is set up and torn down ONCE here.
#  All other modules import GPIO from here instead of directly,
#  which prevents conflicts from multiple setmode/cleanup calls.
# ══════════════════════════════════════════════════════════════

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def cleanup():
    """Call once at program exit to release all GPIO pins."""
    GPIO.cleanup()
