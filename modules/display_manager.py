import cv2
print("Loaded NEW DisplayManager")

class DisplayManager:
    def draw_signal(
    self,
    frame,
    signal,
    current_timer,
    analyzing=False
    ):

        # -------------------------
        # ANALYZING MODE
        # -------------------------
        print("draw_signal called, analyzing =", analyzing)

        if analyzing:

            cv2.circle(
                frame,
                (80,170),
                25,
                (0,255,255),
                -1
            )

            cv2.putText(
                frame,
                "ANALYZING",
                (140,180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2
            )

            return

        # -------------------------
        # NORMAL SIGNALS
        # -------------------------

        color = (0,255,0)

        if signal == "RED":
            color = (0,0,255)

        elif signal == "ORANGE":
            color = (0,165,255)

        cv2.circle(
            frame,
            (80,170),
            25,
            color,
            -1
        )

        cv2.putText(
            frame,
            signal,
            (140,180),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        if current_timer > 0:

            cv2.putText(
                frame,
                f"Timer : {current_timer}",
                (20,250),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255,255,255),
                2
            )