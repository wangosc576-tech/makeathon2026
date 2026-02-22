# ══════════════════════════════════════════════════════════════
#  vision.py  –  Pi Camera capture + MediaPipe hand detection
#  To test standalone: python vision.py
# ══════════════════════════════════════════════════════════════

import cv2
import mediapipe as mp
import numpy as np
from picamera2 import Picamera2
from camera import Camera
import time

# ── MediaPipe setup ───────────────────────────────────────────
_mp_hands = mp.solutions.hands
_mp_draw = mp.solutions.drawing_utils
_hands = _mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6,
)

# ── Finger counting ───────────────────────────────────────────
FINGER_TIPS = [4, 8, 12, 16, 20]
WRIST = 0
MID_BASE = 9

# Per-finger thresholds relative to hand scale.
# Thumb (4) needs a lower value because its range of motion
# relative to the wrist is shorter than the other fingers.
FINGER_THRESHOLDS = {
    4: 0.5,  # thumb
    8: 0.8,  # index
    12: 0.8,  # middle
    16: 0.8,  # ring
    20: 0.8,  # pinky
}


def _to_array(lm):
    return np.array([lm.x, lm.y, lm.z])


def count_fingers(hand_landmarks):
    """Return number of extended fingers (0–5)."""
    lm = hand_landmarks.landmark
    wrist = _to_array(lm[WRIST])
    hand_scale = np.linalg.norm(_to_array(lm[MID_BASE]) - wrist)
    if hand_scale < 1e-5:
        return 0
    count = 0
    for tip_id in FINGER_TIPS:
        threshold = FINGER_THRESHOLDS[tip_id]
        if np.linalg.norm(_to_array(lm[tip_id]) - wrist) > hand_scale * threshold:
            count += 1
    return count


def get_gesture(cam):
    """
    Capture one frame from the camera and return the detected
    finger count, or None if no hand is found.
    Also handles the preview window if not in headless mode.
    """
    frame = cam.capture_array()
    frame = cv2.flip(frame, 1)
    result = _hands.process(frame)  # expects RGB

    finger_count = None

    if result.multi_hand_landmarks:
        for hand_lm in result.multi_hand_landmarks:
            finger_count = count_fingers(hand_lm)
    return finger_count


# ── Standalone test ───────────────────────────────────────────
if __name__ == "__main__":
    print("Vision test – hold up fingers. Ctrl+C to stop.")
    cam = Camera()
    try:
        while True:
            count = get_gesture(cam)
            if count is not None:
                print(f"Fingers detected: {count}")
    except KeyboardInterrupt:
        print("\nDone.")
    finally:
        cam.stop()
