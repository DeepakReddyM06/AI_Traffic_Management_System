from ultralytics import YOLO

class VehicleTracker:

    def __init__(self):

        self.model = YOLO("yolov8s.pt")

        self.vehicle_classes = [2,3,5,7]

    def track(self, frame):

        results = self.model.track(
            frame,
            persist=True,
            imgsz=1920,
            conf=0.6,
            verbose=False
        )

        return results