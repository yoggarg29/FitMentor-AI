from pathlib import Path

import numpy as np
import tensorflow as tf


class FitMentorModel:

    def __init__(
        self,
        model_path="models/fitmentor_lstm.keras",
    ):

        self.model = None

        path = Path(model_path)

        if path.exists():
            self.model = tf.keras.models.load_model(path)

    def is_loaded(self):

        return self.model is not None

    def predict(self, sequence):

        """
        sequence shape

        (30, features)
        """

        if not self.is_loaded():
            return None

        sequence = np.expand_dims(
            sequence,
            axis=0,
        )

        prediction = self.model.predict(
            sequence,
            verbose=0,
        )[0]

        confidence = float(np.max(prediction))

        label = int(np.argmax(prediction))

        return {
            "label": label,
            "confidence": confidence,
            "probabilities": prediction.tolist(),
        }