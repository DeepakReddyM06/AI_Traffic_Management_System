import cv2

cap = cv2.VideoCapture("data/videos/lane2.mp4")

print(
    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
)

cap.release()