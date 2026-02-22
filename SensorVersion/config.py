# ══════════════════════════════════════════════════════════════
#  config.py  –  all shared settings in one place
#  Change values here to adapt to your wiring or setup.
# ══════════════════════════════════════════════════════════════

# GPIO pins
IR_SENSOR_PIN     = 26
TOUCH_PIN         = 12
BUZZER_PIN        = 25

PWM_FREQ          = 1000

# Max time (seconds) between two taps to count as a double tap
DOUBLE_TAP_WINDOW = 0.5

# Minimum time (seconds) between IR toggles to prevent rapid re-triggering
IR_COOLDOWN       = 1.0

# Photos saved here – folder created automatically if missing
PHOTO_SAVE_DIR    = "/home/pi/photos"

# Buzzer beep duration in seconds
BUZZER_DURATION   = 0.3

LED_RED = 16
LED_GREEN = 20
LED_BLUE = 21

CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
JPG_QUALITY = 50
