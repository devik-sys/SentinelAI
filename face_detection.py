import time

import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 
    "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0)
prev_time = 0

while True:

    ret, frame = cam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        1.1,
        4
    )

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Face Detected",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 0, 0),
        2
    )

    timestamp = time.strftime("%H:%M:%S")

    cv2.putText(
        frame,
        timestamp,
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.imshow("SentinelAI Face Detection", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()