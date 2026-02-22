# ══════════════════════════════════════════════════════════════
#  gesture_map.py  –  links finger counts to actions
#  To add a new feature: import its module and add a line here.
# ══════════════════════════════════════════════════════════════

import led

# ── Map finger count → action function ───────────────────────
#  Key   = number of fingers detected
#  Value = function to call (no arguments)
GESTURE_MAP = {
    0: led.off,
    1: led.on,
    # 2: camera.take_photo,     # uncomment when camera.py is added
    # 3: music.play_pause,      # uncomment when music.py is added
    # 4: leds.rainbow,          # uncomment when leds.py is added
}
