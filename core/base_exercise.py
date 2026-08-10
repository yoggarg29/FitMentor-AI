from abc import ABC, abstractmethod
from collections import deque

from core.pose_utils import PoseUtils


class BaseExercise(PoseUtils, ABC):
    ANGLE_DELTA_THRESHOLD = 3
    MIN_CONFIRM_FRAMES = 3

    def __init__(self):
        self.reps = 0
        self.stage = None

        # Motion tracking
        self.angle_history = deque(maxlen=5)
        self.previous_angle = None
        self.movement = "STABLE"

        # Frame confirmation
        self.down_frames = 0
        self.up_frames = 0

    def smooth_angle(self, angle: float) -> float:
        """Apply temporal smoothing to joint angles."""
        self.angle_history.append(angle)
        return sum(self.angle_history) / len(self.angle_history)

    def update_movement(self, angle: float) -> str:
        """Determine movement direction from angle changes."""

        if self.previous_angle is not None:
            delta = angle - self.previous_angle

            if delta < -self.ANGLE_DELTA_THRESHOLD:
                self.movement = "DESCENDING"

            elif delta > self.ANGLE_DELTA_THRESHOLD:
                self.movement = "ASCENDING"

            else:
                self.movement = "STABLE"

        self.previous_angle = angle
        return self.movement

    def reset_tracking(self):
        """Reset common detector state."""

        self.reps = 0
        self.stage = None

        self.angle_history.clear()
        self.previous_angle = None
        self.movement = "STABLE"

        self.down_frames = 0
        self.up_frames = 0

    @abstractmethod
    def process(self, landmarks):
        pass

    @abstractmethod
    def reset(self):
        pass