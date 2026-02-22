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
import camera_workaround
import bash_workaround
def main():
    print("=== Shoulder Companion – Sensor Mode ===")
    oled.init()
    led_on = False
    last_toggle = 0
    last_oled = 0
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
                on_single_tap = oled.switch_state,
                on_double_tap = bash_workaround.capture_picture()
            )
            if (time.time() - last_oled) > 1.5:
                oled.loop()
                last_oled = time.time()

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
