from core.base_exercise import BaseExercise
from core.landmarks import LM


class SquatDetector(BaseExercise):
    REP_BOTTOM_THRESHOLD = 115
    GOOD_DEPTH_THRESHOLD = 100
    STANDING_THRESHOLD = 160

    MIN_VISIBILITY = 0.7
    SIDE_SWITCH_MARGIN = 0.15

    def __init__(self):
        super().__init__()
        self.tracking_side = None

    def reset(self):
        self.reset_tracking()
        self.tracking_side = None

    def process(self, landmarks):

        depth_status = "N/A"

        left_knee_angle = self.calculate_angle(
            self.get_point(landmarks, LM.LEFT_HIP),
            self.get_point(landmarks, LM.LEFT_KNEE),
            self.get_point(landmarks, LM.LEFT_ANKLE),
        )

        right_knee_angle = self.calculate_angle(
            self.get_point(landmarks, LM.RIGHT_HIP),
            self.get_point(landmarks, LM.RIGHT_KNEE),
            self.get_point(landmarks, LM.RIGHT_ANKLE),
        )

        left_visibility = (
            landmarks[LM.LEFT_HIP].visibility
            + landmarks[LM.LEFT_KNEE].visibility
            + landmarks[LM.LEFT_ANKLE].visibility
        ) / 3

        right_visibility = (
            landmarks[LM.RIGHT_HIP].visibility
            + landmarks[LM.RIGHT_KNEE].visibility
            + landmarks[LM.RIGHT_ANKLE].visibility
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

            hip_idx = LM.LEFT_HIP
            knee_idx = LM.LEFT_KNEE
            ankle_idx = LM.LEFT_ANKLE
            shoulder_idx = LM.LEFT_SHOULDER

        else:

            knee_angle = right_knee_angle

            hip_idx = LM.RIGHT_HIP
            knee_idx = LM.RIGHT_KNEE
            ankle_idx = LM.RIGHT_ANKLE
            shoulder_idx = LM.RIGHT_SHOULDER

        knee_angle = self.smooth_angle(knee_angle)
        self.update_movement(knee_angle)

        back_angle = self.calculate_angle(
            self.get_point(landmarks, shoulder_idx),
            self.get_point(landmarks, hip_idx),
            self.get_point(landmarks, knee_idx),
        )

        key_landmark_visible = (
            landmarks[hip_idx].visibility >= self.MIN_VISIBILITY
            and landmarks[knee_idx].visibility >= self.MIN_VISIBILITY
            and landmarks[ankle_idx].visibility >= self.MIN_VISIBILITY
        )

        if key_landmark_visible:

            if knee_angle < self.REP_BOTTOM_THRESHOLD:
                self.down_frames += 1
            else:
                self.down_frames = 0

            if knee_angle > self.STANDING_THRESHOLD:
                self.up_frames += 1
            else:
                self.up_frames = 0

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
            self.movement = "STABLE"

        return {
            "reps": self.reps,
            "knee_angle": int(knee_angle),
            "back_angle": int(back_angle),
            "depth_status": depth_status,
            "movement": self.movement,
        }