import cv2

from modules.vehicle_detection import VehicleDetector

detector = VehicleDetector()

cap = cv2.VideoCapture("data/videos/lane1.mp4")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = detector.detect(frame)

    boxes = results[0].boxes

    for box in boxes:

        cls = int(box.cls[0])

        if cls not in [2,3,5,7]:
            continue

        x1,y1,x2,y2 = map(
            int,
            box.xyxy[0]
        )

        cv2.rectangle(
            frame,
            (x1,y1),
            (x2,y2),
            (0,255,0),
            2
        )

    cv2.imshow(
        "Vehicle Detection Test",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()