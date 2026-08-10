from core.base_exercise import BaseExercise
from core.landmarks import LM


class LungesDetector(BaseExercise):
    DOWN_THRESHOLD = 100
    UP_THRESHOLD = 160
    LEG_SELECTION_THRESHOLD = 145

    MIN_VISIBILITY = 0.7
    TORSO_LEAN_TOLERANCE = 0.10

    def __init__(self):
        super().__init__()
        self.active_leg = None

    def reset(self) -> None:
        self.reset_tracking()
        self.active_leg = None

    def process(self, landmarks) -> dict:
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

        left_visible = (
            landmarks[LM.LEFT_HIP].visibility >= self.MIN_VISIBILITY
            and landmarks[LM.LEFT_KNEE].visibility >= self.MIN_VISIBILITY
            and landmarks[LM.LEFT_ANKLE].visibility >= self.MIN_VISIBILITY
        )

        right_visible = (
            landmarks[LM.RIGHT_HIP].visibility >= self.MIN_VISIBILITY
            and landmarks[LM.RIGHT_KNEE].visibility >= self.MIN_VISIBILITY
            and landmarks[LM.RIGHT_ANKLE].visibility >= self.MIN_VISIBILITY
        )

        if self.active_leg is None:
            if (
                left_visible
                and left_knee_angle <= self.LEG_SELECTION_THRESHOLD
                and (
                    not right_visible
                    or left_knee_angle < right_knee_angle
                )
            ):
                self.active_leg = "LEFT"
                self.angle_history.clear()
                self.previous_angle = None

            elif (
                right_visible
                and right_knee_angle <= self.LEG_SELECTION_THRESHOLD
                and (
                    not left_visible
                    or right_knee_angle < left_knee_angle
                )
            ):
                self.active_leg = "RIGHT"
                self.angle_history.clear()
                self.previous_angle = None

        if self.active_leg == "LEFT":
            front_knee_angle = left_knee_angle

            front_hip_idx = LM.LEFT_HIP
            front_knee_idx = LM.LEFT_KNEE
            front_ankle_idx = LM.LEFT_ANKLE
            shoulder_idx_for_torso = LM.LEFT_SHOULDER

            key_landmarks_visible = left_visible

        elif self.active_leg == "RIGHT":
            front_knee_angle = right_knee_angle

            front_hip_idx = LM.RIGHT_HIP
            front_knee_idx = LM.RIGHT_KNEE
            front_ankle_idx = LM.RIGHT_ANKLE
            shoulder_idx_for_torso = LM.RIGHT_SHOULDER

            key_landmarks_visible = right_visible

        else:
            front_knee_angle = min(
                left_knee_angle,
                right_knee_angle,
            )

            torso_angle = 0
            torso_stability = "READY"

            self.movement = "STABLE"

            return {
                "reps": self.reps,
                "front_knee_angle": int(front_knee_angle),
                "torso_angle": torso_angle,
                "torso_stability": torso_stability,
                "movement": self.movement,
                "active_leg": "NONE",
            }

        front_knee_angle = self.smooth_angle(
            front_knee_angle
        )

        self.update_movement(front_knee_angle)

        if key_landmarks_visible:
            if front_knee_angle <= self.DOWN_THRESHOLD:
                self.down_frames += 1
            else:
                self.down_frames = 0

            if front_knee_angle >= self.UP_THRESHOLD:
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

                self.active_leg = None

                self.angle_history.clear()
                self.previous_angle = None
                self.movement = "STABLE"

        else:
            self.movement = "STABLE"
            self.down_frames = 0
            self.up_frames = 0

        torso_angle = self.calculate_angle(
            self.get_point(
                landmarks,
                shoulder_idx_for_torso,
            ),
            self.get_point(
                landmarks,
                front_hip_idx,
            ),
            self.get_point(
                landmarks,
                front_knee_idx,
            ),
        )

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
            shoulder_mid_x = (
                landmarks[LM.LEFT_SHOULDER].x
                + landmarks[LM.RIGHT_SHOULDER].x
            ) / 2

            hip_mid_x = (
                landmarks[LM.LEFT_HIP].x
                + landmarks[LM.RIGHT_HIP].x
            ) / 2

            lateral_offset = abs(
                shoulder_mid_x - hip_mid_x
            )

            if lateral_offset <= self.TORSO_LEAN_TOLERANCE:
                torso_stability = "STABLE"
            else:
                torso_stability = "LATERAL LEAN"

        else:
            torso_stability = "N/A"

        return {
            "reps": self.reps,
            "front_knee_angle": int(front_knee_angle),
            "torso_angle": int(torso_angle),
            "torso_stability": torso_stability,
            "movement": self.movement,
            "active_leg": self.active_leg or "NONE",
        }