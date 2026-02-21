import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Set pin 17 as input
SENSOR_PIN = 17
GPIO.setup(SENSOR_PIN, GPIO.IN)

print("IR Sensor Ready...")
try:
    while True:
        if GPIO.input(SENSOR_PIN):
            print("No Object")
        else:
            print("Yes Object")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()

