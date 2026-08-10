from core.base_exercise import BaseExercise
from core.landmarks import LM


class ShoulderPressDetector(BaseExercise):
    REP_UP_THRESHOLD = 150
    REP_DOWN_THRESHOLD = 90

    FULL_EXTENSION_THRESHOLD = 160
    NEAR_EXTENSION_THRESHOLD = 130

    MIN_VISIBILITY = 0.7
    ARM_SYMMETRY_TOLERANCE = 15

    def __init__(self):
        super().__init__()

    def reset(self) -> None:
        self.reset_tracking()

    def process(self, landmarks) -> dict:
        left_elbow_angle = self.calculate_angle(
            self.get_point(landmarks, LM.LEFT_SHOULDER),
            self.get_point(landmarks, LM.LEFT_ELBOW),
            self.get_point(landmarks, LM.LEFT_WRIST),
        )

        right_elbow_angle = self.calculate_angle(
            self.get_point(landmarks, LM.RIGHT_SHOULDER),
            self.get_point(landmarks, LM.RIGHT_ELBOW),
            self.get_point(landmarks, LM.RIGHT_WRIST),
        )

        key_landmarks_visible = (
            landmarks[LM.LEFT_SHOULDER].visibility >= self.MIN_VISIBILITY
            and landmarks[LM.LEFT_ELBOW].visibility >= self.MIN_VISIBILITY
            and landmarks[LM.LEFT_WRIST].visibility >= self.MIN_VISIBILITY
            and landmarks[LM.RIGHT_SHOULDER].visibility >= self.MIN_VISIBILITY
            and landmarks[LM.RIGHT_ELBOW].visibility >= self.MIN_VISIBILITY
            and landmarks[LM.RIGHT_WRIST].visibility >= self.MIN_VISIBILITY
        )

        if key_landmarks_visible:
            elbow_angle = (
                left_elbow_angle + right_elbow_angle
            ) / 2

            elbow_angle = self.smooth_angle(elbow_angle)
            self.update_movement(elbow_angle)

            if elbow_angle >= self.REP_UP_THRESHOLD:
                self.up_frames += 1
            else:
                self.up_frames = 0

            if elbow_angle <= self.REP_DOWN_THRESHOLD:
                self.down_frames += 1
            else:
                self.down_frames = 0

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

        else:
            elbow_angle = 0
            self.movement = "STABLE"
            self.up_frames = 0
            self.down_frames = 0

        arm_difference = abs(
            left_elbow_angle - right_elbow_angle
        )

        if elbow_angle < self.REP_DOWN_THRESHOLD:
            symmetry_status = "READY"

        elif arm_difference <= self.ARM_SYMMETRY_TOLERANCE:
            symmetry_status = "BALANCED"

        else:
            symmetry_status = "UNEVEN PRESS"

        if elbow_angle >= self.FULL_EXTENSION_THRESHOLD:
            extension_status = "FULL EXTENSION"

        elif elbow_angle >= self.NEAR_EXTENSION_THRESHOLD:
            extension_status = "NEARLY EXTENDED"

        elif elbow_angle >= self.REP_DOWN_THRESHOLD:
            extension_status = "PRESSING"

        else:
            extension_status = "START POSITION"

        return {
            "reps": self.reps,
            "elbow_angle": int(elbow_angle),
            "extension_status": extension_status,
            "symmetry_status": symmetry_status,
            "movement": self.movement,
        }