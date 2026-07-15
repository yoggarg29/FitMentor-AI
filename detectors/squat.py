from core.base_exercise import BaseExercise
from collections import deque

class SquatDetector(BaseExercise):
    REP_BOTTOM_THRESHOLD = 115
    GOOD_DEPTH_THRESHOLD = 100
    STANDING_THRESHOLD = 160
    MIN_VISIBILITY = 0.7
    ANGLE_DELTA_THRESHOLD = 3
    SIDE_SWITCH_MARGIN = 0.15

    LEFT_HIP = 23
    LEFT_KNEE = 25
    LEFT_ANKLE = 27

    RIGHT_HIP = 24
    RIGHT_KNEE = 26
    RIGHT_ANKLE = 28

    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12

    MIN_CONFIRM_FRAMES = 3

    def __init__(self):
        super().__init__()
        self.angle_history = deque(maxlen=5)
        self.previous_angle = None
        self.movement = "STABLE"
        self.tracking_side = None
        self.down_frames = 0
        self.up_frames = 0
        self.MIN_CONFIRM_FRAMES = 3


    def reset(self):
        self.reps=0
        self.stage=None
        self.angle_history.clear()
        self.previous_angle = None
        self.movement = "STABLE"
        self.tracking_side = None
        self.down_frames = 0
        self.up_frames = 0


    def process(self, landmarks):
        depth_status = "N/A"
        left_knee_angle=self.calculate_angle(
            self.get_point(landmarks,self.LEFT_HIP),
            self.get_point(landmarks,self.LEFT_KNEE),
            self.get_point(landmarks,self.LEFT_ANKLE),
        )

        right_knee_angle=self.calculate_angle(
            self.get_point(landmarks,self.RIGHT_HIP),
            self.get_point(landmarks,self.RIGHT_KNEE),
            self.get_point(landmarks,self.RIGHT_ANKLE),
        )

        left_visibility = (
            landmarks[self.LEFT_HIP].visibility
            + landmarks[self.LEFT_KNEE].visibility
            + landmarks[self.LEFT_ANKLE].visibility
        ) / 3

        right_visibility = (
            landmarks[self.RIGHT_HIP].visibility
            + landmarks[self.RIGHT_KNEE].visibility
            + landmarks[self.RIGHT_ANKLE].visibility
        ) / 3

        if self.tracking_side is None:
            self.tracking_side = (
                "LEFT"
                if left_visibility >= right_visibility
                else "RIGHT"
            )

        elif (
            self.tracking_side == "LEFT"
            and right_visibility > left_visibility + self.SIDE_SWITCH_MARGIN
        ):
            self.tracking_side = "RIGHT"
            self.angle_history.clear()
            self.previous_angle = None

        elif (
            self.tracking_side == "RIGHT"
            and left_visibility > right_visibility + self.SIDE_SWITCH_MARGIN
        ):
            self.tracking_side = "LEFT"
            self.angle_history.clear()
            self.previous_angle = None

        if self.tracking_side == "LEFT":
            knee_angle = left_knee_angle
            hip_idx = self.LEFT_HIP
            knee_idx = self.LEFT_KNEE
            ankle_idx = self.LEFT_ANKLE
            shoulder_idx = self.LEFT_SHOULDER

        else:
            knee_angle = right_knee_angle
            hip_idx = self.RIGHT_HIP
            knee_idx = self.RIGHT_KNEE
            ankle_idx = self.RIGHT_ANKLE
            shoulder_idx = self.RIGHT_SHOULDER

        self.angle_history.append(knee_angle)
        smoothed_angle = sum(self.angle_history) / len(self.angle_history)

        if self.previous_angle is not None:
            delta = smoothed_angle - self.previous_angle

            if delta < -self.ANGLE_DELTA_THRESHOLD:
                self.movement = "DESCENDING"
            elif delta > self.ANGLE_DELTA_THRESHOLD:
                self.movement = "ASCENDING"
            else:
                self.movement = "STABLE"

        self.previous_angle = smoothed_angle
        knee_angle = smoothed_angle

        back_angle=self.calculate_angle(
            self.get_point(landmarks,shoulder_idx),
            self.get_point(landmarks,hip_idx),
            self.get_point(landmarks,knee_idx)
        )

        key_landmark_visible=landmarks[hip_idx].visibility>= self.MIN_VISIBILITY and landmarks[knee_idx].visibility >= self.MIN_VISIBILITY and landmarks[ankle_idx].visibility >= self.MIN_VISIBILITY

        if key_landmark_visible:

            if knee_angle < self.REP_BOTTOM_THRESHOLD:
                self.down_frames += 1
            else:
                self.down_frames = 0

            if knee_angle > self.STANDING_THRESHOLD:
                self.up_frames += 1
            else:
                self.up_frames = 0

            # Confirm bottom position
            if (
                self.down_frames >= self.MIN_CONFIRM_FRAMES
                and self.stage != "down"
            ):
                self.stage = "down"

            if (
                self.up_frames >= self.MIN_CONFIRM_FRAMES
                and self.stage == "down"
            ):
                self.stage = "up"
                self.reps += 1

                self.down_frames = 0
                self.up_frames = 0
            if knee_angle <= self.GOOD_DEPTH_THRESHOLD:
                depth_status = "GOOD DEPTH"

            elif knee_angle <= self.REP_BOTTOM_THRESHOLD:
                depth_status = "SHALLOW DEPTH"

            elif knee_angle < self.STANDING_THRESHOLD:
                depth_status = "MOVING"

            else:
                depth_status = "STANDING"
        else:
            self.movement="STABLE"

        return {
            "reps":self.reps,
            "knee_angle":int(knee_angle),
            "back_angle":int(back_angle),
            "depth_status":depth_status,
            "movement": self.movement
        }
