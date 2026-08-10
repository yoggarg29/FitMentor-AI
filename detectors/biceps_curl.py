import math

from core.base_exercise import BaseExercise
from core.landmarks import LM


class BicepsCurlDetector(BaseExercise):
    UP_THRESHOLD = 50
    DOWN_THRESHOLD = 160

    MIN_VISIBILITY = 0.7

    ELBOW_DRIFT_TOLERANCE = 0.06
    SWING_THRESHOLD = 8

    def __init__(self):
        super().__init__()
        self.torso_baseline_angle = None
        self.tracking_side = None

    def reset(self) -> None:
        self.reset_tracking()
        self.torso_baseline_angle = None
        self.tracking_side = None

    def process(self, landmarks) -> dict:
        left_vis = landmarks[LM.LEFT_ELBOW].visibility
        right_vis = landmarks[LM.RIGHT_ELBOW].visibility

        if self.tracking_side is None:
            if left_vis >= right_vis:
                self.tracking_side = "LEFT"
            else:
                self.tracking_side = "RIGHT"

        if self.tracking_side == "LEFT":
            shoulder_idx = LM.LEFT_SHOULDER
            elbow_idx = LM.LEFT_ELBOW
            wrist_idx = LM.LEFT_WRIST

        else:
            shoulder_idx = LM.RIGHT_SHOULDER
            elbow_idx = LM.RIGHT_ELBOW
            wrist_idx = LM.RIGHT_WRIST

        elbow_angle = self.calculate_angle(
            self.get_point(landmarks, shoulder_idx),
            self.get_point(landmarks, elbow_idx),
            self.get_point(landmarks, wrist_idx),
        )

        elbow_angle = self.smooth_angle(elbow_angle)
        self.update_movement(elbow_angle)

        key_landmarks_visible = (
            landmarks[shoulder_idx].visibility >= self.MIN_VISIBILITY
            and landmarks[elbow_idx].visibility >= self.MIN_VISIBILITY
            and landmarks[wrist_idx].visibility >= self.MIN_VISIBILITY
        )

        if key_landmarks_visible:
            if elbow_angle <= self.UP_THRESHOLD:
                self.up_frames += 1
            else:
                self.up_frames = 0

            if elbow_angle >= self.DOWN_THRESHOLD:
                self.down_frames += 1
            else:
                self.down_frames = 0

            if (
                self.up_frames >= self.MIN_CONFIRM_FRAMES
                and self.stage != "up"
            ):
                self.stage = "up"

            if (
                self.down_frames >= self.MIN_CONFIRM_FRAMES
                and self.stage == "up"
            ):
                self.stage = "down"
                self.reps += 1

                self.up_frames = 0
                self.down_frames = 0

        else:
            self.movement = "STABLE"
            self.up_frames = 0
            self.down_frames = 0

        shoulder_x = landmarks[shoulder_idx].x
        elbow_x = landmarks[elbow_idx].x

        elbow_drift = abs(elbow_x - shoulder_x)

        if elbow_drift <= self.ELBOW_DRIFT_TOLERANCE:
            shoulder_status = "STABLE"
        else:
            shoulder_status = "ELBOW DRIFTING"

        shoulder_mid_x = (
            landmarks[LM.LEFT_SHOULDER].x
            + landmarks[LM.RIGHT_SHOULDER].x
        ) / 2

        shoulder_mid_y = (
            landmarks[LM.LEFT_SHOULDER].y
            + landmarks[LM.RIGHT_SHOULDER].y
        ) / 2

        hip_mid_x = (
            landmarks[LM.LEFT_HIP].x
            + landmarks[LM.RIGHT_HIP].x
        ) / 2

        hip_mid_y = (
            landmarks[LM.LEFT_HIP].y
            + landmarks[LM.RIGHT_HIP].y
        ) / 2

        dx = shoulder_mid_x - hip_mid_x
        dy = shoulder_mid_y - hip_mid_y

        torso_angle = self._safe_angle(dx, dy)

        torso_landmarks_visible = (
            landmarks[LM.LEFT_SHOULDER].visibility
            >= self.MIN_VISIBILITY
            and landmarks[LM.RIGHT_SHOULDER].visibility
            >= self.MIN_VISIBILITY
            and landmarks[LM.LEFT_HIP].visibility
            >= self.MIN_VISIBILITY
            and landmarks[LM.RIGHT_HIP].visibility
            >= self.MIN_VISIBILITY
        )

        if torso_landmarks_visible:
            if self.torso_baseline_angle is None:
                self.torso_baseline_angle = torso_angle

            torso_deviation = abs(
                torso_angle - self.torso_baseline_angle
            )

            if torso_deviation > self.SWING_THRESHOLD:
                swing_status = "SWINGING"
            else:
                swing_status = "NO SWING"

        else:
            swing_status = "N/A"

        return {
            "reps": self.reps,
            "elbow_angle": int(elbow_angle),
            "shoulder_status": shoulder_status,
            "swing_status": swing_status,
            "movement": self.movement,
        }

    def _safe_angle(self, dx, dy):
        if dy == 0:
            return 0.0

        return math.degrees(
            math.atan2(abs(dx), abs(dy))
        )