class DatasetCollector:

    def __init__(
        self,
        extractor,
        builder,
    ):

        self.extractor = extractor
        self.builder = builder

        self.recording = False
        self.current_label = None

    def start(self, label):

        self.current_label = label
        self.recording = True

    def stop(self):

        self.recording = False

    def process(self, landmarks):

        if not self.recording:
            return

        features = self.extractor.extract(
            landmarks
        )

        self.builder.add_sample(
            features,
            self.current_label,
        )