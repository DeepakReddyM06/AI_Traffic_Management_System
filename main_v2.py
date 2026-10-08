import cv2
import time

from modules.vehicle_detection import VehicleDetector
from modules.vehicle_counter import VehicleCounter
from modules.signal_manager import SignalManager
from modules.display_manager import DisplayManager

# -----------------------------------
# INITIALIZE MODULES
# -----------------------------------

detector = VehicleDetector()
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
# STATES
# -----------------------------------

STATE_ANALYZING = 0
STATE_GREEN = 1
STATE_ORANGE = 2

current_state = STATE_ANALYZING

# -----------------------------------
# VARIABLES
# -----------------------------------
next_lane = None

current_lane = None

left_count = 0
right_count = 0

current_timer = 0
next_timer = 0

analysis_start = time.time()
last_second = time.time()
orange_start = 0

frame1_frozen = None
frame2_frozen = None

analysis_done = False
orange_done = False

def count_vehicles(frame, detector, counter):

    results = detector.detect(frame)

    count = 0

    for box in results[0].boxes:

        cls = int(box.cls[0])

        if cls not in [2, 3, 5, 7]:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if counter.inside_roi(cx, cy):

            count += 1

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

    return count

# -----------------------------------
# MAIN LOOP
# -----------------------------------

while True:

    if current_state == STATE_ANALYZING:

        if not analysis_done:

            # Reset both videos
            cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
            cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)

            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            frame1_frozen = frame1.copy()
            frame2_frozen = frame2.copy()

            left_count = count_vehicles(
                frame1_frozen,
                detector,
                lane1_counter
            )

            right_count = count_vehicles(
                frame2_frozen,
                detector,
                lane2_counter
            )

            analysis_done = True
            analysis_start = time.time()



        frame1 = frame1_frozen.copy()
        frame2 = frame2_frozen.copy()

        if left_count >= right_count:
            current_lane = "LEFT"
            current_timer = max(left_count,5)

        else:
            current_lane = "RIGHT"
            next_timer = max(right_count,5)

        if time.time() - analysis_start >= 3:

            signals.reset_signals()

            if current_lane == "LEFT":
                signals.set_left_green()
            else:
                signals.set_right_green()

            last_second = time.time()

            analysis_done = False

            current_state = STATE_GREEN

    elif current_state == STATE_GREEN:

        # -----------------------------
        # PLAY CURRENT LANE
        # -----------------------------

        if current_lane == "LEFT":

            ret1, frame1 = cap1.read()

            if not ret1:
                cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret1, frame1 = cap1.read()

            frame2 = frame2_frozen.copy()

        else:

            ret2, frame2 = cap2.read()

            if not ret2:
                cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret2, frame2 = cap2.read()

            frame1 = frame1_frozen.copy()

        # -----------------------------
        # TIMER
        # -----------------------------

        # Timer countdown
        if time.time() - last_second >= 1 and current_timer > 0:

            current_timer -= 1
            last_second = time.time()

        # Enter orange only once
        if current_timer == 3 and not orange_done:

            orange_done = True
            orange_start = time.time()
            print("Entered ORANGE at", orange_start)
            current_state = STATE_ORANGE

    elif current_state == STATE_ORANGE:
        print("ORANGE TIMER =", time.time() - orange_start)
        if orange_done:

            orange_done = False

            if current_lane == "LEFT":

                signals.reset_signals()
                signals.set_right_orange()

                cap2.set(cv2.CAP_PROP_POS_FRAMES,0)

                ret2, frame2 = cap2.read()

                frame2_frozen = frame2.copy()

                right_count = count_vehicles(
                    frame2_frozen,
                    detector,
                    lane2_counter
                )

                next_timer = right_count

            else:

                signals.reset_signals()
                signals.set_left_orange()

                cap1.set(cv2.CAP_PROP_POS_FRAMES,0)

                ret1, frame1 = cap1.read()

                frame1_frozen = frame1.copy()

                left_count = count_vehicles(
                    frame1_frozen,
                    detector,
                    lane1_counter
                )

                next_timer = left_count

        # Wait for 3 seconds
        if time.time() - orange_start >= 3:
            print("SWITCHING TO GREEN")
            # Switch lane
            orange_done = False

            current_timer = next_timer

            if current_lane == "LEFT":
                current_lane = "RIGHT"
            else:
                current_lane = "LEFT"

            signals.reset_signals()

            if current_lane == "LEFT":
                signals.set_left_green()
            else:
                signals.set_right_green()

            last_second = time.time()

            current_state = STATE_GREEN
            if current_lane == "LEFT":

                cap1.set(cv2.CAP_PROP_POS_FRAMES,0)

            else:

                cap2.set(cv2.CAP_PROP_POS_FRAMES,0)
    # -----------------------------
    # DRAW ROI
    # -----------------------------

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

    # -----------------------------
    # DRAW TITLES
    # -----------------------------

    cv2.putText(
        frame1,
        "LEFT LANE",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        2
    )

    cv2.putText(
        frame2,
        "RIGHT LANE",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        2
    )

    cv2.putText(
    frame1,
    f"Count: {left_count}",
    (20,80),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0,255,255),
    2
    )

    cv2.putText(
        frame2,
        f"Count: {right_count}",
        (20,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,255),
        2
        )

    display.draw_signal(
    frame1,
    signals.left_signal,
    current_timer,
    current_state == STATE_ANALYZING
    )

    display.draw_signal(
        frame2,
        signals.right_signal,
        current_timer,
        current_state == STATE_ANALYZING
    )
    # -----------------------------
    # SHOW WINDOW
    # -----------------------------

    combined = cv2.hconcat([frame1, frame2])

    cv2.imshow(
        "AI Traffic Management System",
        combined
    )

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap1.release()
cap2.release()

cv2.destroyAllWindows()