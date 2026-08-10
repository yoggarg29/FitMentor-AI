from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from services.ai.preprocessor import FeaturePreprocessor


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.callbacks import EarlyStopping

from sklearn.model_selection import train_test_split


class ModelTrainer:

    def __init__(
        self,
        sequence_length=30,
    ):

        self.sequence_length = sequence_length

        self.preprocessor = FeaturePreprocessor()
        
        self.encoder = LabelEncoder()

    ##########################################################
    # Load CSV
    ##########################################################

    def load_dataset(
        self,
        csv_path,
    ):

        return pd.read_csv(csv_path)

    ##########################################################
    # Prepare Data
    ##########################################################

    def prepare_data(
        self,
        dataframe,
    ):

        X = dataframe.drop(
            columns=["label"]
        )

        y = dataframe["label"]

        X = self.preprocessor.scaler.fit_transform(X)

        y = self.encoder.fit_transform(y)

        return X, y

    ##########################################################
    # Create Temporal Sequences
    ##########################################################

    def create_sequences(
        self,
        X,
        y,
    ):

        X_seq = []
        y_seq = []

        for i in range(
            len(X) - self.sequence_length
        ):

            X_seq.append(
                X[
                    i:i + self.sequence_length
                ]
            )

            y_seq.append(
                y[
                    i + self.sequence_length
                ]
            )

        return (
            np.array(X_seq),
            np.array(y_seq),
        )

    ##########################################################
    # LSTM Model
    ##########################################################

    def build_model(
        self,
        input_shape,
        classes,
    ):

        model = Sequential()

        model.add(
            LSTM(
                64,
                input_shape=input_shape,
            )
        )

        model.add(
            Dropout(0.3)
        )

        model.add(
            Dense(
                64,
                activation="relu",
            )
        )

        model.add(
            Dropout(0.3)
        )

        model.add(
            Dense(
                classes,
                activation="softmax",
            )
        )

        model.compile(

            optimizer="adam",

            loss="sparse_categorical_crossentropy",

            metrics=["accuracy"],
        )

        return model

    ##########################################################
    # Train
    ##########################################################

    def train(
        self,
        csv_path,
        model_path="models/fitmentor_lstm.keras",
    ):

        df = self.load_dataset(
            csv_path,
        )

        X, y = self.prepare_data(
            df,
        )

        X, y = self.create_sequences(
            X,
            y,
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            shuffle=True,
        )

        model = self.build_model(
            input_shape=X_train.shape[1:],
            classes=len(
                self.encoder.classes_
            ),
        )

        callback = EarlyStopping(

            monitor="val_loss",

            patience=5,

            restore_best_weights=True,
        )

        model.fit(

            X_train,

            y_train,

            validation_data=(
                X_test,
                y_test,
            ),

            epochs=50,

            batch_size=32,

            callbacks=[callback],
        )

        Path("models").mkdir(
            exist_ok=True
        )

        model.save(model_path)

        joblib.dump(
            self.scaler,
            "models/scaler.pkl",
        )

        joblib.dump(
            self.encoder,
            "models/label_encoder.pkl",
        )

        loss, accuracy = model.evaluate(
            X_test,
            y_test,
            verbose=0,
        )

        print(
            f"Accuracy : {accuracy:.3f}"
        )