from core.pose_utils import PoseUtils
from core.landmarks import LM


class FeatureExtractor(PoseUtils):

    def extract(self, landmarks):
        features = {}

        features.update(
            self._extract_joint_angles(landmarks)
        )

        features.update(
            self._extract_lengths(landmarks)
        )

        features.update(
            self._extract_symmetry(landmarks, features)
        )

        features.update(
            self._extract_posture(landmarks)
        )

        return features


    # Joint Angles


    def _extract_joint_angles(self, landmarks):

        features = {}

        features["left_elbow_angle"] = self.calculate_angle(
            self.get_point(landmarks, LM.LEFT_SHOULDER),
            self.get_point(landmarks, LM.LEFT_ELBOW),
            self.get_point(landmarks, LM.LEFT_WRIST),
        )

        features["right_elbow_angle"] = self.calculate_angle(
            self.get_point(landmarks, LM.RIGHT_SHOULDER),
            self.get_point(landmarks, LM.RIGHT_ELBOW),
            self.get_point(landmarks, LM.RIGHT_WRIST),
        )

        features["left_knee_angle"] = self.calculate_angle(
            self.get_point(landmarks, LM.LEFT_HIP),
            self.get_point(landmarks, LM.LEFT_KNEE),
            self.get_point(landmarks, LM.LEFT_ANKLE),
        )

        features["right_knee_angle"] = self.calculate_angle(
            self.get_point(landmarks, LM.RIGHT_HIP),
            self.get_point(landmarks, LM.RIGHT_KNEE),
            self.get_point(landmarks, LM.RIGHT_ANKLE),
        )

        return features


    # Body Lengths


    def _extract_lengths(self, landmarks):

        features = {}

        shoulder_mid = self.midpoint(
            self.get_point(landmarks, LM.LEFT_SHOULDER),
            self.get_point(landmarks, LM.RIGHT_SHOULDER),
        )

        hip_mid = self.midpoint(
            self.get_point(landmarks, LM.LEFT_HIP),
            self.get_point(landmarks, LM.RIGHT_HIP),
        )

        ankle_mid = self.midpoint(
            self.get_point(landmarks, LM.LEFT_ANKLE),
            self.get_point(landmarks, LM.RIGHT_ANKLE),
        )

        head = self.get_point(landmarks, LM.NOSE)

        features["shoulder_width"] = self.distance(
            self.get_point(landmarks, LM.LEFT_SHOULDER),
            self.get_point(landmarks, LM.RIGHT_SHOULDER),
        )

        features["hip_width"] = self.distance(
            self.get_point(landmarks, LM.LEFT_HIP),
            self.get_point(landmarks, LM.RIGHT_HIP),
        )

        features["torso_length"] = self.distance(
            shoulder_mid,
            hip_mid,
        )

        features["body_height"] = self.distance(
            head,
            ankle_mid,
        )

        features["left_arm_length"] = (
            self.distance(
                self.get_point(landmarks, LM.LEFT_SHOULDER),
                self.get_point(landmarks, LM.LEFT_ELBOW),
            )
            +
            self.distance(
                self.get_point(landmarks, LM.LEFT_ELBOW),
                self.get_point(landmarks, LM.LEFT_WRIST),
            )
        )

        features["right_arm_length"] = (
            self.distance(
                self.get_point(landmarks, LM.RIGHT_SHOULDER),
                self.get_point(landmarks, LM.RIGHT_ELBOW),
            )
            +
            self.distance(
                self.get_point(landmarks, LM.RIGHT_ELBOW),
                self.get_point(landmarks, LM.RIGHT_WRIST),
            )
        )

        return features


    # Symmetry Features


    def _extract_symmetry(
        self,
        landmarks,
        features,
    ):

        symmetry = {}

        symmetry["shoulder_symmetry"] = abs(
            landmarks[LM.LEFT_SHOULDER].y
            -
            landmarks[LM.RIGHT_SHOULDER].y
        )

        symmetry["hip_symmetry"] = abs(
            landmarks[LM.LEFT_HIP].y
            -
            landmarks[LM.RIGHT_HIP].y
        )

        symmetry["elbow_symmetry"] = abs(
            features["left_elbow_angle"]
            -
            features["right_elbow_angle"]
        )

        symmetry["knee_symmetry"] = abs(
            features["left_knee_angle"]
            -
            features["right_knee_angle"]
        )

        symmetry["arm_length_difference"] = abs(
            features["left_arm_length"]
            -
            features["right_arm_length"]
        )

        return symmetry


    # Posture Features


    def _extract_posture(self, landmarks):

        posture = {}

        shoulder_mid = self.midpoint(
            self.get_point(landmarks, LM.LEFT_SHOULDER),
            self.get_point(landmarks, LM.RIGHT_SHOULDER),
        )

        hip_mid = self.midpoint(
            self.get_point(landmarks, LM.LEFT_HIP),
            self.get_point(landmarks, LM.RIGHT_HIP),
        )

        posture["torso_angle"] = self.calculate_angle(
            shoulder_mid,
            hip_mid,
            (
                hip_mid[0],
                hip_mid[1] + 1,
            ),
        )

        posture["lateral_offset"] = abs(
            shoulder_mid[0]
            -
            hip_mid[0]
        )

        return posture