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
        1.3,
        5
    )

    for (x, y, w, h) in faces:

        if len(faces) == 0:
            alert_sent = False

        face = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(face)

        if confidence < 80:
            name = "Devi"
        else:

            name = "Unknown"

            if not alert_sent:

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                filename = f"unknown_faces/unknown_{timestamp}.jpg"

                cv2.imwrite(
                    filename,
                    frame
                )

                print(f"Saved: {filename}")
                
                with open("intrusion_log.txt", "a") as log:

                    log.write(
                        f"{datetime.now()} - Unknown Person Detected - {filename}\n"
                    )

                print("ALERT: Unknown Person Detected!")

                alert_sent = True
            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

        cv2.putText(
            frame,
            name,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Face Recognition",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
