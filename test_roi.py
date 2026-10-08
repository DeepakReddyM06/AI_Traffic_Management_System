import cv2

from modules.vehicle_detection import VehicleDetector
from modules.vehicle_counter import VehicleCounter

detector = VehicleDetector()
counter = VehicleCounter()

cap = cv2.VideoCapture("data/videos/lane1.mp4")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = detector.detect(frame)

    count = 0

    boxes = results[0].boxes

    for box in boxes:

        cls = int(box.cls[0])

        if cls not in [2,3,5,7]:
            continue

        x1,y1,x2,y2 = map(int, box.xyxy[0])

        center_x = (x1+x2)//2
        center_y = (y1+y2)//2

        if counter.inside_roi(
            center_x,
            center_y
        ):

            count += 1

            color = (0,255,0)

        else:

            color = (0,0,255)

        cv2.rectangle(
            frame,
            (x1,y1),
            (x2,y2),
            color,
            2
        )

    cv2.rectangle(
        frame,
        (counter.roi_x1,counter.roi_y1),
        (counter.roi_x2,counter.roi_y2),
        (255,0,0),
        2
    )

    cv2.putText(
        frame,
        f"ROI Count: {count}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,255),
        2
    )

    cv2.imshow(
        "ROI Counter Test",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()