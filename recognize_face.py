import cv2
import os
from datetime import datetime

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

alert_sent = False

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        face = gray[
            y:y+h,
            x:x+w
        ]

        face = cv2.resize(
            face,
            (200, 200)
        )

        label, confidence = recognizer.predict(
            face
        )

        print(
            f"Label: {label} | Raw Confidence: {confidence}"
        )

        match_percent = max(
            0,
            min(
                100,
                round(100 - confidence, 1)
            )
        )

        if confidence < 85:

            name = "ACCESS GRANTED"

            color = (
                0,
                255,
                0
            )

            alert_sent = False

        else:

            name = "INTRUDER ALERT"

            color = (
                0,
                0,
                255
            )

            if not alert_sent:

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )

                filename = (
                    f"snapshots/intruder_{timestamp}.jpg"
                )

                cv2.imwrite(
                    filename,
                    frame
                )

                with open(
                    "intrusion_log.txt",
                    "a"
                ) as log:

                    log.write(
                        f"{datetime.now()} - Unknown Person Detected - {filename}\n"
                    )

                print(
                    "ALERT: Unknown Person Detected!"
                )

                alert_sent = True

        display_text = (
            f"{name} "
            f"{match_percent}%"
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            color,
            2
        )

        cv2.putText(
            frame,
            display_text,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    if len(faces) == 0:

        alert_sent = False

    cv2.imshow(
        "SentinelAI",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()