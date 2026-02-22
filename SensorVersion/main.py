# ══════════════════════════════════════════════════════════════
#  main.py  –  entry point, ties all modules together
#  Run with: python main.py
# ══════════════════════════════════════════════════════════════

import time
import gpio_manager   # must be imported first – sets up GPIO.setmode once
import led 
import ir_sensor
import touch_sensor
import oled
from camera_workaround import capture_picture
def main():
    print("=== Shoulder Companion – Sensor Mode ===")
    print("  IR sensor   → wave to toggle flashlight on/off")
    print("  Touch       → single tap  = take a photo")
    print("  Touch       → double tap  = buzzer beep")
    print("Ctrl+C to stop.\n")
    counter = 0
    oled.init()
    led_on = False
    last_toggle = 0
    try:
        while True:
            
            if (ir_sensor.detected()):
            # IR sensor: new detection toggles the flashlight
                now = time.time()
                if now - last_toggle > 0.5:
                    if (led_on):
                        led.off()
                    else:
                        led.on()
                    led_on = not led_on
                    last_toggle = time.time()
            # Touch sensor: single = photo, double = buzzer
            touch_sensor.check(
                on_single_tap = capture_picture,
                on_double_tap = oled.switch_state
            )
            oled.loop()

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        # Each module cleans up its own hardware
        led.off()
        # ONE call releases all GPIO pins
        gpio_manager.cleanup()
        oled.clear()
        print("Cleaned up. Goodbye!")

if __name__ == "__main__":
    main()
