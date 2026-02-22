# ══════════════════════════════════════════════════════════════
#  config.py  –  all shared settings in one place
#  Change values here to adapt to your wiring or setup.
# ══════════════════════════════════════════════════════════════

# GPIO pins
FLASHLIGHT_PIN    = 18
IR_SENSOR_PIN     = 24
TOUCH_PIN         = 23
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
