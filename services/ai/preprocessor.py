from pathlib import Path

import joblib
from sklearn.preprocessing import StandardScaler


class FeaturePreprocessor:

    def __init__(self):
        self.scaler = StandardScaler()

    def fit_transform(self, X):
        return self.scaler.fit_transform(X)

    def transform(self, X):
        return self.scaler.transform(X)

    def save(
        self,
        path="models/scaler.pkl",
    ):
        Path("models").mkdir(exist_ok=True)
        joblib.dump(self.scaler, path)

    def load(
        self,
        path="models/scaler.pkl",
    ):
        self.scaler = joblib.load(path)