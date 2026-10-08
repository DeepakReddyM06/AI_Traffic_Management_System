from ultralytics import YOLO

class VehicleDetector:

    def __init__(self):
        self.model = YOLO("yolov8n.pt")

        self.vehicle_classes = [2, 3, 5, 7]

    def detect(self, frame):

        results = self.model(
            frame,
            conf=0.4,
            verbose=False
        )

        return results