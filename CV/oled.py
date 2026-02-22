# ══════════════════════════════════════════════════════════════
#  oled.py  –  SSD1306 128x64 OLED over I2C
#  Displays a random inspirational message on double tap.
#  To test standalone: python oled.py
#
#  Wiring (I2C):
#    OLED VCC  → 3.3V (Pin 1)
#    OLED GND  → GND  (Pin 6)
#    OLED SDA  → SDA  (Pin 3, GPIO 2)
#    OLED SCL  → SCL  (Pin 5, GPIO 3)
#
#  I2C address is 0x3C on most SSD1306 modules.
#  If your screen doesn't show anything, try 0x3D below.
# ══════════════════════════════════════════════════════════════

import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import time

# ── I2C config ────────────────────────────────────────────────
I2C_ADDRESS = 0x3C   # change to 0x3D if screen doesn't respond

# ── Screen dimensions ─────────────────────────────────────────
WIDTH  = 128
HEIGHT = 64

# ── Inspirational messages ────────────────────────────────────
MESSAGES = [
    "You are capable of amazing things.",
    "Every step forward counts.",
    "Believe in yourself.",
    "Make today count.",
    "You've got this.",
    "Stay curious. Stay bold.",
    "Small steps, big dreams.",
    "Your potential is endless.",
    "Be the energy you want.",
    "Courage starts with one step.",
    "You are enough.",
    "Dream big. Start small.",
    "Keep going. You're closer than you think.",
    "Progress, not perfection.",
    "The best is yet to come.",
]

# ── Internal state ────────────────────────────────────────────
_display      = None
_last_message = None  # avoids showing the same message twice in a row

def _get_font():
    """
    Load the default PIL font safely across Pillow versions.
    Pillow 10+ supports a size parameter; older versions do not.
    Always returns a usable font object.
    """
    try:
        return ImageFont.load_default(size=10)  # Pillow 10+
    except TypeError:
        return ImageFont.load_default()          # Pillow <10

def _measure_line_height(font):
    """
    Measure the actual pixel height of the font rather than
    hardcoding a value that could be wrong across Pillow versions.
    """
    dummy = Image.new("1", (WIDTH, HEIGHT))
    draw  = ImageDraw.Draw(dummy)
    bbox  = draw.textbbox((0, 0), "A", font=font)
    return bbox[3] - bbox[1] + 2  # height + 2px line spacing

def init():
    """Initialise the OLED display over I2C. Call once at startup."""
    global _display
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
    except ValueError as e:
        print(f"[OLED] I2C init failed – is I2C enabled? Run: sudo raspi-config")
        print(f"[OLED] Error: {e}")
        return
    _display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=I2C_ADDRESS)
    clear()
    print(f"[OLED] Ready on I2C address {hex(I2C_ADDRESS)}.")

def clear():
    """Blank the screen."""
    if _display is None:
        return
    _display.fill(0)
    _display.show()

def show_message(message=None):
    """
    Display a random inspirational message.
    Pass a specific string to override the random pick.
    """
    global _last_message

    if _display is None:
        print("[OLED] Not initialised – call oled.init() first.")
        return

    # Pick a random message, avoiding repeating the last one
    if message is None:
        choices = [m for m in MESSAGES if m != _last_message]
        message = random.choice(choices)
    _last_message = message

    # Guard against empty message
    if not message.strip():
        print("[OLED] Empty message, skipping.")
        return

    font        = _get_font()
    line_height = _measure_line_height(font)

    # Word-wrap to fit 128px wide (approx 21 chars at default font size)
    lines = textwrap.wrap(message, width=21)
    if not lines:
        print("[OLED] Message produced no lines after wrapping, skipping.")
        return

    # Build image – exactly WIDTH x HEIGHT to match the display buffer
    image        = Image.new("1", (WIDTH, HEIGHT))
    draw         = ImageDraw.Draw(image)
    total_height = len(lines) * line_height
    y            = max(0, (HEIGHT - total_height) // 2)

    for line in lines:
        bbox       = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x          = max(0, (WIDTH - text_width) // 2)  # clamp so text never goes off-screen
        draw.text((x, y), line, font=font, fill=255)
        y += line_height

    _display.image(image)
    _display.show()
    print(f"[OLED] Showing: \"{message}\"")

def cleanup():
    """Blank the screen on exit."""
    clear()

# ── Standalone test ───────────────────────────────────────────
if __name__ == "__main__":
    init()
    print("Cycling through 3 random messages...")
    for _ in range(3):
        show_message()
        time.sleep(3)
    cleanup()
    print("Done.")
