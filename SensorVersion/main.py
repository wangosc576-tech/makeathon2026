# ══════════════════════════════════════════════════════════════
#  main.py  –  entry point, ties all modules together
#  Run with: python main.py
# ══════════════════════════════════════════════════════════════

import time
import gpio_manager   # must be imported first – sets up GPIO.setmode once
import flashlight
import ir_sensor
import touch_sensor
import camera
import buzzer

def main():
    print("=== Shoulder Companion – Sensor Mode ===")
    print("  IR sensor   → wave to toggle flashlight on/off")
    print("  Touch       → single tap  = take a photo")
    print("  Touch       → double tap  = buzzer beep")
    print("Ctrl+C to stop.\n")

    camera.init()

    try:
        while True:
            # IR sensor: new detection toggles the flashlight
            ir_sensor.check_toggle(flashlight.toggle)

            # Touch sensor: single = photo, double = buzzer
            touch_sensor.check(
                on_single_tap = camera.take_photo,
                on_double_tap = buzzer.double_beep,
            )

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        # Each module cleans up its own hardware
        flashlight.cleanup()
        buzzer.cleanup()
        camera.cleanup()
        # ONE call releases all GPIO pins
        gpio_manager.cleanup()
        print("Cleaned up. Goodbye!")

if __name__ == "__main__":
    main()
