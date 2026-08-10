from core.base_exercise import BaseExercise
from core.landmarks import LM


class PushUpDetector(BaseExercise):
    DOWN_THRESHOLD = 90
    UP_THRESHOLD = 160

    MIN_VISIBILITY = 0.7

    HIP_DEVIATION_TOLERANCE = 0.04

    BODY_STRAIGHT = 160
    BODY_SLIGHT_BEND = 140

    def __init__(self):
        super().__init__()

    def reset(self) -> None:
        self.reset_tracking()

    def process(self, landmarks) -> dict:
        left_vis = landmarks[LM.LEFT_ELBOW].visibility
        right_vis = landmarks[LM.RIGHT_ELBOW].visibility

        if left_vis >= right_vis:
            shoulder_idx = LM.LEFT_SHOULDER
            elbow_idx = LM.LEFT_ELBOW
            wrist_idx = LM.LEFT_WRIST
            hip_idx = LM.LEFT_HIP
            ankle_idx = LM.LEFT_ANKLE
        else:
            shoulder_idx = LM.RIGHT_SHOULDER
            elbow_idx = LM.RIGHT_ELBOW
            wrist_idx = LM.RIGHT_WRIST
            hip_idx = LM.RIGHT_HIP
            ankle_idx = LM.RIGHT_ANKLE

        # Elbow angle
        elbow_angle = self.calculate_angle(
            self.get_point(landmarks, shoulder_idx),
            self.get_point(landmarks, elbow_idx),
            self.get_point(landmarks, wrist_idx),
        )

        elbow_angle = self.smooth_angle(elbow_angle)
        self.update_movement(elbow_angle)

        # Body alignment angle
        body_angle = self.calculate_angle(
            self.get_point(landmarks, shoulder_idx),
            self.get_point(landmarks, hip_idx),
            self.get_point(landmarks, ankle_idx),
        )

        # Hip deviation from shoulder-ankle body line
        shoulder_x = landmarks[shoulder_idx].x
        shoulder_y = landmarks[shoulder_idx].y

        hip_x = landmarks[hip_idx].x
        hip_y = landmarks[hip_idx].y

        ankle_x = landmarks[ankle_idx].x
        ankle_y = landmarks[ankle_idx].y

        body_dx = ankle_x - shoulder_x
        body_dy = ankle_y - shoulder_y

        body_length = (body_dx ** 2 + body_dy ** 2) ** 0.5

        if body_length > 0:
            hip_deviation = (
                body_dx * (hip_y - shoulder_y)
                - body_dy * (hip_x - shoulder_x)
            ) / body_length

            normalized_hip_deviation = hip_deviation / body_length
        else:
            normalized_hip_deviation = 0.0

        # Landmark visibility
        key_landmarks_visible = (
            landmarks[shoulder_idx].visibility >= self.MIN_VISIBILITY
            and landmarks[elbow_idx].visibility >= self.MIN_VISIBILITY
            and landmarks[wrist_idx].visibility >= self.MIN_VISIBILITY
            and landmarks[hip_idx].visibility >= self.MIN_VISIBILITY
            and landmarks[ankle_idx].visibility >= self.MIN_VISIBILITY
        )

        # Rep counting with frame confirmation
        if key_landmarks_visible:
            if elbow_angle <= self.DOWN_THRESHOLD:
                self.down_frames += 1
            else:
                self.down_frames = 0

            if elbow_angle >= self.UP_THRESHOLD:
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

        else:
            self.movement = "STABLE"
            self.down_frames = 0
            self.up_frames = 0

        # Body alignment feedback
        if body_angle >= self.BODY_STRAIGHT:
            body_alignment = "Straight"
        elif body_angle >= self.BODY_SLIGHT_BEND:
            body_alignment = "Slight Bend"
        else:
            body_alignment = "Poor Form"

        # Hip position feedback
        if abs(normalized_hip_deviation) <= self.HIP_DEVIATION_TOLERANCE:
            hip_status = "LEVEL"
        elif normalized_hip_deviation > self.HIP_DEVIATION_TOLERANCE:
            hip_status = "SAGGING"
        else:
            hip_status = "PIKED UP"

        return {
            "reps": self.reps,
            "elbow_angle": int(elbow_angle),
            "body_alignment": body_alignment,
            "hip_status": hip_status,
            "movement": self.movement,
        }