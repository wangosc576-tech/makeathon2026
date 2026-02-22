# ══════════════════════════════════════════════════════════════
#  debouncer.py  –  prevents accidental gesture triggers
# ══════════════════════════════════════════════════════════════

from config import DEBOUNCE_FRAMES


class GestureDebouncer:
    """
    Requires the same gesture to appear in N consecutive frames
    before it fires. Also prevents the same gesture from firing
    repeatedly while held.
    """

    def __init__(self):
        self.buffer = []
        self.last_fired = None

    def update(self, gesture):
        """
        Pass in the latest detected gesture (or None).
        Returns the confirmed gesture if it just became stable,
        otherwise returns None.
        """
        self.buffer.append(gesture)
        if len(self.buffer) > DEBOUNCE_FRAMES:
            self.buffer.pop(0)

        if (
            len(self.buffer) == DEBOUNCE_FRAMES
            and self.buffer.count(gesture) == DEBOUNCE_FRAMES
            and gesture != self.last_fired
        ):
            self.last_fired = gesture
            # note - depeending on action structure may need to change this allow repeats
            return gesture

        return None

    def clear(self):
        self.buffer.clear()
        self.last_fired = None
