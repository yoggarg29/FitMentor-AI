import math


class PoseUtils:

    @staticmethod
    def get_point(landmarks, idx):
        landmark = landmarks[idx]
        return (landmark.x, landmark.y)

    @staticmethod
    def calculate_angle(a, b, c):
        """
        Returns angle ABC in degrees.
        """

        ax = a[0] - b[0]
        ay = a[1] - b[1]

        cx = c[0] - b[0]
        cy = c[1] - b[1]

        dot = ax * cx + ay * cy

        mag_a = math.sqrt(ax * ax + ay * ay)
        mag_c = math.sqrt(cx * cx + cy * cy)

        if mag_a == 0 or mag_c == 0:
            return 0.0

        cos_angle = max(
            -1.0,
            min(1.0, dot / (mag_a * mag_c)),
        )

        return math.degrees(math.acos(cos_angle))

    @staticmethod
    def distance(p1, p2):
        return math.sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
        )

    @staticmethod
    def midpoint(p1, p2):
        return (
            (p1[0] + p2[0]) / 2,
            (p1[1] + p2[1]) / 2,
        )

    @staticmethod
    def normalize_distance(value, reference):

        if reference == 0:
            return 0.0

        return value / reference