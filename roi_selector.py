import cv2

def mouse(event, x, y, flags, param):

    if event == cv2.EVENT_MOUSEMOVE:
        print(x, y)

cap = cv2.VideoCapture("data/videos/lane1.mp4")

ret, frame = cap.read()

cv2.namedWindow("Lane1")
cv2.setMouseCallback("Lane1", mouse)

while True:

    cv2.imshow("Lane1", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()