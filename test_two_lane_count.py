import cv2

from modules.vehicle_detection import VehicleDetector
from modules.vehicle_counter import VehicleCounter

detector = VehicleDetector()

# Lane 1 ROI
lane1_counter = VehicleCounter(
    319, 12,
    833, 274
)

# Lane 2 ROI
lane2_counter = VehicleCounter(
    345, 18,
    827, 249
)

cap1 = cv2.VideoCapture("data/videos/lane1.mp4")
cap2 = cv2.VideoCapture("data/videos/lane2.mp4")

while True:

    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        break

    count1 = 0
    count2 = 0

    # --------------------
    # LANE 1 DETECTION
    # --------------------

    results1 = detector.detect(frame1)

    for box in results1[0].boxes:

        cls = int(box.cls[0])

        # car, motorcycle, bus, truck
        if cls not in [2, 3, 5, 7]:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if lane1_counter.inside_roi(cx, cy):

            count1 += 1

            cv2.rectangle(
                frame1,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

    # --------------------
    # LANE 2 DETECTION
    # --------------------

    results2 = detector.detect(frame2)

    for box in results2[0].boxes:

        cls = int(box.cls[0])

        # car, motorcycle, bus, truck
        if cls not in [2, 3, 5, 7]:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if lane2_counter.inside_roi(cx, cy):

            count2 += 1

            cv2.rectangle(
                frame2,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

    # --------------------
    # DRAW ROI
    # --------------------

    cv2.rectangle(
        frame1,
        (319, 12),
        (833, 274),
        (255, 0, 0),
        2
    )

    cv2.rectangle(
        frame2,
        (345, 18),
        (827, 249),
        (255, 0, 0),
        2
    )

    # --------------------
    # LANE LABELS
    # --------------------

    cv2.putText(
        frame1,
        "LEFT LANE",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame2,
        "RIGHT LANE",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    # --------------------
    # VEHICLE COUNTS
    # --------------------

    cv2.putText(
        frame1,
        f"Count: {count1}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame2,
        f"Count: {count2}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    # --------------------
    # COMBINE WINDOWS
    # --------------------

    combined = cv2.hconcat([frame1, frame2])

    cv2.imshow(
        "AI Traffic Management System",
        combined
    )

    if cv2.waitKey(1) == 27:
        break

cap1.release()
cap2.release()

cv2.destroyAllWindows()