from collections import deque
import numpy as np


class SequenceBuffer:

    def __init__(self, sequence_length=30):
        self.sequence_length = sequence_length
        self.buffer = deque(maxlen=sequence_length)

    def reset(self):
        self.buffer.clear()

    def add(self, feature_vector):
        """
        feature_vector -> dictionary returned by FeatureExtractor
        """
        self.buffer.append(list(feature_vector.values()))

    def is_ready(self):
        return len(self.buffer) == self.sequence_length

    def get_sequence(self):
        if not self.is_ready():
            return None

        return np.array(
            self.buffer,
            dtype=np.float32,
        )