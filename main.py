import cv2
import time

from modules.vehicle_detection import VehicleDetector
from modules.vehicle_counter import VehicleCounter
from modules.traffic_controller import TrafficController
from modules.signal_manager import SignalManager
from modules.display_manager import DisplayManager


# -----------------------------------
# INITIALIZE MODULES
# -----------------------------------

detector = VehicleDetector()
controller = TrafficController()
signals = SignalManager()
display = DisplayManager()

# -----------------------------------
# ROI DEFINITIONS
# -----------------------------------

lane1_counter = VehicleCounter(
    319, 12,
    833, 274
)

lane2_counter = VehicleCounter(
    345, 18,
    827, 249
)

# -----------------------------------
# LOAD VIDEOS
# -----------------------------------

cap1 = cv2.VideoCapture(
    "data/videos/lane1.mp4"
)

cap2 = cv2.VideoCapture(
    "data/videos/lane2.mp4"
)

# -----------------------------------
# VARIABLES
# -----------------------------------

current_lane = "LEFT"

analysis_phase = True
analysis_start = time.time()

current_timer = 0
last_second = time.time()

frozen_frame1 = None
frozen_frame2 = None

frame_count = 0

fps = int(cap1.get(cv2.CAP_PROP_FPS))
frame_timer = 0

next_timer = 5
# -----------------------------------
# MAIN LOOP
# -----------------------------------

while True:

    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    # Restart videos if finished

    for _ in range(2):
        cap1.grab()
        cap2.grab()

    if not ret1:
        cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret1, frame1 = cap1.read()

    if not ret2:
        cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret2, frame2 = cap2.read()

    # -----------------------------------
    # INITIAL ANALYSIS (2 sec)
    # -----------------------------------

    if analysis_phase:

        # Freeze both videos

        if frozen_frame1 is None:
            frozen_frame1 = frame1.copy()

        if frozen_frame2 is None:
            frozen_frame2 = frame2.copy()

        frame1 = frozen_frame1.copy()
        frame2 = frozen_frame2.copy()

    else:

        # Freeze opposite lane

        if current_lane == "LEFT":

            if frozen_frame2 is None:
                frozen_frame2 = frame2.copy()

            frame2 = frozen_frame2.copy()
            frozen_frame1 = None

        else:

            if frozen_frame1 is None:
                frozen_frame1 = frame1.copy()

            frame1 = frozen_frame1.copy()
            frozen_frame2 = None

    # -----------------------------------
    # VEHICLE COUNTING
    # -----------------------------------

    count1 = 0
    count2 = 0

    # LEFT LANE

    results1 = detector.detect(frame1)

    for box in results1[0].boxes:

        cls = int(box.cls[0])

        if cls not in [2, 3, 5, 7]:
            continue

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0]
        )

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

    # RIGHT LANE

    results2 = detector.detect(frame2)

    for box in results2[0].boxes:

        cls = int(box.cls[0])

        if cls not in [2, 3, 5, 7]:
            continue

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0]
        )

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

    # -----------------------------------
    # ANALYSIS PHASE
    # -----------------------------------

    analyzing = False

    if analysis_phase:

        analyzing = True

        if time.time() - analysis_start >= 2:

            current_timer = next_timer
            orange_processed = False

            signals.reset_signals()
            signals.set_left_green()

            analysis_phase = False
            last_second = time.time()

    # -----------------------------------
    # NORMAL SIGNAL OPERATION
    # -----------------------------------

    else:

        # Countdown

        # Countdown

        if time.time() - last_second >= 1 and current_timer > 0:

            current_timer -= 1
            last_second = time.time()

        # Orange phase

        if 0 < current_timer <= 3:

            if current_lane == "LEFT":

                signals.set_right_orange()

                # Reset RIGHT video once
                if current_timer == 3:
                    cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)

            else:

                signals.set_left_orange()

                # Reset LEFT video once
                if current_timer == 3:
                    cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Switch lane

        # Orange phase

    if 0 < current_timer <= 3:

        if current_lane == "LEFT":

            signals.set_right_orange()

            if current_timer == 3 and not orange_processed:

                orange_processed = True

                cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)

                ret_temp, temp_frame = cap2.read()

                if ret_temp:

                    temp_results = detector.detect(temp_frame)

                    temp_count = 0

                    for box in temp_results[0].boxes:

                        cls = int(box.cls[0])

                        if cls not in [2, 3, 5, 7]:
                            continue

                        x1, y1, x2, y2 = map(
                            int,
                            box.xyxy[0]
                        )

                        cx = (x1 + x2) // 2
                        cy = (y1 + y2) // 2

                        if lane2_counter.inside_roi(
                            cx,
                            cy
                        ):
                            temp_count += 1

                    next_timer = max(
                        5,
                        min(temp_count, 30)
                    )

        else:

            signals.set_left_orange()

            if current_timer == 3 and not orange_processed:

                orange_processed = True

                cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)

                ret_temp, temp_frame = cap1.read()

                if ret_temp:

                    temp_results = detector.detect(temp_frame)

                    temp_count = 0

                    for box in temp_results[0].boxes:

                        cls = int(box.cls[0])

                        if cls not in [2, 3, 5, 7]:
                            continue

                        x1, y1, x2, y2 = map(
                            int,
                            box.xyxy[0]
                        )

                        cx = (x1 + x2) // 2
                        cy = (y1 + y2) // 2

                        if lane1_counter.inside_roi(
                            cx,
                            cy
                        ):
                            temp_count += 1

                    next_timer = max(
                        5,
                        min(temp_count, 30)
                    )

    # -----------------------------------
    # DRAW ROI
    # -----------------------------------

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

    # -----------------------------------
    # LABELS
    # -----------------------------------

    cv2.putText(
        frame1,
        "LEFT LANE",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame2,
        "RIGHT LANE",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame1,
        f"Count: {count1}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame2,
        f"Count: {count2}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    # -----------------------------------
    # SIGNAL DISPLAY
    # -----------------------------------

    display.draw_signal(
        frame1,
        signals.left_signal,
        current_timer,
        analyzing and current_lane == "LEFT"
    )

    display.draw_signal(
        frame2,
        signals.right_signal,
        current_timer,
        analyzing and current_lane == "RIGHT"
    )

    # -----------------------------------
    # SHOW WINDOW
    # -----------------------------------

    combined = cv2.hconcat(
        [frame1, frame2]
    )

    cv2.imshow(
        "AI Traffic Management System",
        combined
    )

    if cv2.waitKey(1) == 27:
        break

# -----------------------------------
# CLEANUP
# -----------------------------------

cap1.release()
cap2.release()

cv2.destroyAllWindows()