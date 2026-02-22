# ══════════════════════════════════════════════════════════════
#  config.py  –  all shared settings in one place
#  Change values here to adapt to your wiring or setup.
# ══════════════════════════════════════════════════════════════

# GPIO pins
FLASHLIGHT_PIN = 18
IR_SENSOR_PIN = 24
PWM_FREQ = 1000


# How long (seconds) gesture detection stays awake after
# the IR sensor last detected something
IR_COOLDOWN = 2.0

# Number of consecutive frames a gesture must be held
# before it fires
DEBOUNCE_FRAMES = 8

# Camera resolution – lower = faster processing on Pi Zero 2 W
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
JPG_QUALITY = 50

# LED pins
LED_RED = 37
LED_GREEN = 38
LED_BLUE = 40
