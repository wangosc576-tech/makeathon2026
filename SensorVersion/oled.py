# ══════════════════════════════════════════════════════════════
#  oled.py  -  SSD1306 128x64 OLED over I2C
#  To test standalone: python oled.py
#
#  Wiring (I2C):
#    OLED VCC  -> 3.3V (Pin 1)
#    OLED GND  -> GND  (Pin 6)
#    OLED SDA  -> SDA  (Pin 3, GPIO 2)
#    OLED SCL  -> SCL  (Pin 5, GPIO 3)
# ══════════════════════════════════════════════════════════════

import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import time

# ── I2C config ────────────────────────────────────────────────
I2C_ADDRESS = 0x3C

# ── Screen dimensions ─────────────────────────────────────────
WIDTH = 128
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

# ── ASCII artworks ────────────────────────────────────────────
# All quotes removed from art to avoid string delimiter clashes
ARTWORKS = [
    (
        " __         __\n"
        "/  \\.-   -./  \\\n"
        "\\    -   -    /\n"
        " |   o   o   |\n"
        " \\  .-~~~-.  /\n"
        "  -\\__Y__/-\n"
        "     `---`"
    ),
    (
        r"\|/       (__)" + "\n"
        r"  `\------(oo)" + "\n"
        r"    ||    (__)" + "\n"
        r"    ||w--||  \|/" + "\n"
        r" \|/"
    ),
    (
        "  ___________\n"
        " |  _______  |\n"
        " | |  o o  | |\n"
        " | |   ^   | |\n"
        " | |  \\_/  | |\n"
        " |___________|\n"
    ),
    (
        " _._     _,-..-._\n"
        "(,-.._.,(       |\\`-/|\n"
        "    `-.-  \\ )-( , o o)\n"
        "          `-    \\`_.-\n"
    ),
]

# ── Internal state ────────────────────────────────────────────
_display = None
_last_message = None
oled_state = "OFF"


def _get_font():
    try:
        return ImageFont.load_default(size=10)  # Pillow 10+
    except TypeError:
        return ImageFont.load_default()  # Pillow <10


def _measure_line_height(font):
    dummy = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(dummy)
    bbox = draw.textbbox((0, 0), "A", font=font)
    return bbox[3] - bbox[1] + 2


def init():
    global _display
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
    except ValueError as e:
        print(f"[OLED] I2C init failed - is I2C enabled? Run: sudo raspi-config")
        print(f"[OLED] Error: {e}")
        return
    _display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=I2C_ADDRESS)
    clear()
    print(f"[OLED] Ready on I2C address {hex(I2C_ADDRESS)}.")


def clear():
    if _display is None:
        return
    _display.fill(0)
    _display.show()


def loop():
    if oled_state == "OFF":
        return
    elif oled_state == "MESSAGE":
        show_message()
    elif oled_state == "ART":
        show_art()


def switch_state():
    global oled_state
    if oled_state == "OFF":
        oled_state = "MESSAGE"
    elif oled_state == "MESSAGE":
        oled_state = "ART"
    else:
        oled_state = "OFF"
    print(f"[OLED] State: {oled_state}")


def draw_ascii(art):
    if _display is None:
        print("[OLED] Not initialised - call oled.init() first.")
        return
    font = _get_font()
    line_height = _measure_line_height(font)
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    for i, line in enumerate(art.splitlines()):
        draw.text((0, i * line_height), line, font=font, fill=255)
    _display.image(image)
    _display.show()


def show_art():
    art = ARTWORKS[random.randint(0, len(ARTWORKS) - 1)]
    draw_ascii(art)


def show_message(message=None):
    global _last_message
    if _display is None:
        print("[OLED] Not initialised - call oled.init() first.")
        return
    if message is None:
        choices = [m for m in MESSAGES if m != _last_message]
        message = random.choice(choices)
    _last_message = message
    if not message.strip():
        return
    font = _get_font()
    line_height = _measure_line_height(font)
    lines = textwrap.wrap(message, width=21)
    if not lines:
        return
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    total_height = len(lines) * line_height
    y = max(0, (HEIGHT - total_height) // 2)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = max(0, (WIDTH - text_width) // 2)
        draw.text((x, y), line, font=font, fill=255)
        y += line_height
    _display.image(image)
    _display.show()
    print(f'[OLED] Showing: "{message}"')


def cleanup():
    clear()


# ── Standalone test ───────────────────────────────────────────
if __name__ == "__main__":
    init()
    print("Cycling through states...")
    for _ in range(6):
        switch_state()
        loop()
        time.sleep(3)
    cleanup()
    print("Done.")
