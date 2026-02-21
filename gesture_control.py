import cv2
import mediapipe as mp
import RPi.GPIO as GPIO
import numpy as np
from picamera2 import Picamera2
import time

# ══════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════
FLASHLIGHT_PIN = 18
IR_SENSOR_PIN  = 24      # GPIO pin for IR sensor output
PWM_FREQ       = 1000

# Set to True if running without a monitor attached.
HEADLESS       = False

# How long (seconds) to keep gesture detection running after
# the IR sensor stops detecting. Prevents flickering on/off
# if the hand briefly leaves the IR sensor's range.
IR_COOLDOWN    = 2.0

# ══════════════════════════════════════════════════════════════
#  GPIO SETUP
# ══════════════════════════════════════════════════════════════
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLASHLIGHT_PIN, GPIO.OUT)
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)   # IR sensor as input

flashlight_pwm = GPIO.PWM(FLASHLIGHT_PIN, PWM_FREQ)
flashlight_pwm.start(0)

def set_flashlight(brightness):
    """Set flashlight brightness 0–100."""
    flashlight_pwm.ChangeDutyCycle(max(0, min(100, brightness)))

def ir_detected():
    """
    Returns True if the IR sensor is detecting something nearby.
    Most IR obstacle sensors output LOW when triggered, HIGH when clear.
    Flip the logic (== GPIO.HIGH) if yours behaves the opposite way.
    """
    return GPIO.input(IR_SENSOR_PIN) == GPIO.LOW

# ══════════════════════════════════════════════════════════════
#  PICAMERA2 SETUP
# ══════════════════════════════════════════════════════════════
def init_camera():
    cam = Picamera2()
    config = cam.create_preview_configuration(
        main={"format": "RGB888", "size": (320, 240)}
    )
    cam.configure(config)
    cam.start()
    time.sleep(0.5)  # let camera warm up
    return cam

# ══════════════════════════════════════════════════════════════
#  ACTIONS  –  add new actions here as functions
# ══════════════════════════════════════════════════════════════

def action_all_off():
    """Fist (0) – turn everything off."""
    print("[ACTION] All OFF")
    set_flashlight(0)
    # TODO: stop music, turn off RGB LEDs, etc.

def action_flashlight_on():
    """1 finger – turn flashlight on."""
    print("[ACTION] Flashlight ON")
    set_flashlight(100)

# ── Add future actions below this line ────────────────────────
# def action_take_photo():   ...
# def action_play_music():   ...
# def action_rgb_rainbow():  ...
# ──────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════
#  GESTURE MAP
# ══════════════════════════════════════════════════════════════
GESTURE_MAP = {
    0: action_all_off,
    1: action_flashlight_on,
    # 2: action_take_photo,
    # 3: action_play_music,
    # 4: action_rgb_rainbow,
}


# ══════════════════════════════════════════════════════════════
#  FINGER COUNTING
#  Uses wrist-to-fingertip distance so it works at any angle.
# ══════════════════════════════════════════════════════════════
FINGER_TIPS = [4, 8, 12, 16, 20]
WRIST       = 0
MID_BASE    = 9

# Threshold multipliers per finger tip ID.
# The thumb (tip 4) has a shorter range of motion relative to the wrist
# than the other fingers, so it needs a lower threshold to register as
# extended. Tune THUMB_THRESHOLD if you still get miscounts.
FINGER_THRESHOLDS = {
    4:  0.5,   # thumb  – shorter range of motion, needs lower threshold
    8:  0.8,   # index
    12: 0.8,   # middle
    16: 0.8,   # ring
    20: 0.8,   # pinky
}

def landmark_to_array(lm):
    return np.array([lm.x, lm.y, lm.z])

def count_fingers(hand_landmarks):
    lm = hand_landmarks.landmark
    wrist      = landmark_to_array(lm[WRIST])
    mid_base   = landmark_to_array(lm[MID_BASE])
    hand_scale = np.linalg.norm(mid_base - wrist)
    if hand_scale < 1e-5:
        return 0
    count = 0
    for tip_id in FINGER_TIPS:
        tip       = landmark_to_array(lm[tip_id])
        threshold = FINGER_THRESHOLDS[tip_id]
        if np.linalg.norm(tip - wrist) > hand_scale * threshold:
            count += 1
    return count


# ══════════════════════════════════════════════════════════════
#  DEBOUNCE
# ══════════════════════════════════════════════════════════════
DEBOUNCE_FRAMES = 8

class GestureDebouncer:
    def __init__(self, threshold):
        self.threshold  = threshold
        self.buffer     = []
        self.last_fired = None

    def update(self, gesture):
        self.buffer.append(gesture)
        if len(self.buffer) > self.threshold:
            self.buffer.pop(0)
        if (len(self.buffer) == self.threshold
                and self.buffer.count(gesture) == self.threshold
                and gesture != self.last_fired):
            self.last_fired = gesture
            return gesture
        return None

    def clear(self):
        self.buffer.clear()
        self.last_fired = None


# ══════════════════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════════════════
def main():
    mp_hands = mp.solutions.hands
    mp_draw  = mp.solutions.drawing_utils
    hands    = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6
    )

    print("Starting Pi Camera...")
    cam = init_camera()

    debouncer      = GestureDebouncer(DEBOUNCE_FRAMES)
    active_label   = "None"
    last_ir_time   = 0       # timestamp of last IR detection
    gesture_active = False   # whether we're currently processing gestures

    print("=== Shoulder Companion – Gesture Control ===")
    print(f"Headless mode : {HEADLESS}")
    print(f"IR cooldown   : {IR_COOLDOWN}s")
    print("Mapped gestures:")
    for fingers, fn in GESTURE_MAP.items():
        print(f"  {fingers} finger(s) → {fn.__name__}")
    print("Waiting for IR trigger...\n")

    try:
        while True:

            # ── IR Wake Check ──────────────────────────────────────
            if ir_detected():
                last_ir_time   = time.time()
                gesture_active = True

            # Stay active for IR_COOLDOWN seconds after last detection
            elif gesture_active:
                if time.time() - last_ir_time > IR_COOLDOWN:
                    gesture_active = False
                    debouncer.clear()
                    print("[IR] Hand gone – gesture detection sleeping.")

            # ── Sleep mode: skip frame capture entirely ────────────
            if not gesture_active:
                time.sleep(0.05)  # light sleep to avoid busy-waiting
                continue

            # ── Active mode: run gesture detection ─────────────────
            frame  = cam.capture_array()
            frame  = cv2.flip(frame, 1)
            result = hands.process(frame)

            raw_gesture = None

            if result.multi_hand_landmarks:
                for hand_lm in result.multi_hand_landmarks:
                    raw_gesture = count_fingers(hand_lm)

                confirmed = debouncer.update(raw_gesture)
                if confirmed is not None and confirmed in GESTURE_MAP:
                    GESTURE_MAP[confirmed]()
                    active_label = GESTURE_MAP[confirmed].__name__
            else:
                debouncer.clear()

            # ── Display (skipped in headless mode) ─────────────────
            if not HEADLESS:
                display = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                if result.multi_hand_landmarks:
                    for hand_lm in result.multi_hand_landmarks:
                        mp_draw.draw_landmarks(display, hand_lm, mp_hands.HAND_CONNECTIONS)
                    cv2.putText(display, f"Fingers: {raw_gesture}", (10, 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
                ir_label = "IR: ACTIVE" if gesture_active else "IR: sleeping"
                cv2.putText(display, ir_label, (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 255, 255) if gesture_active else (100, 100, 100), 2)
                cv2.putText(display, f"Active: {active_label}", (10, 220),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                cv2.imshow("Shoulder Companion", display)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            # ───────────────────────────────────────────────────────

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        action_all_off()
        cam.stop()
        if not HEADLESS:
            cv2.destroyAllWindows()
        flashlight_pwm.stop()
        GPIO.cleanup()
        print("Cleaned up. Goodbye!")

if __name__ == "__main__":
    main()
