from gpiozero import RGBLED


# Define GPIO pins for Red, Green, and Blue
# Red=Pin 22, Green=Pin 27, Blue=Pin 17
led = RGBLED(red=22, green=27, blue=17)


def on():
    led.color = (1, 1, 1)


def off():
    led.color = (0, 0, 0)


# ── Standalone test ───────────────────────────────────────────
if __name__ == "__main__":
    import time

    print("LED test – turning on for 3 seconds...")
    on()
    time.sleep(3)
    off()
    print("Done.")
