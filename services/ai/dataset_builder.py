import csv
import os


class DatasetBuilder:

    def __init__(self, save_path):

        self.save_path = save_path

        self.header_written = os.path.exists(save_path)

    def add_sample(
        self,
        features,
        label,
    ):

        row = dict(features)
        row["label"] = label

        file_exists = os.path.exists(self.save_path)

        with open(
            self.save_path,
            "a",
            newline="",
        ) as f:

            writer = csv.DictWriter(
                f,
                fieldnames=row.keys(),
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow(row)