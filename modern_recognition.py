import pickle
import cv2
import numpy as np

with open(
    "face_encodings.pkl",
    "rb"
) as file:

    database = pickle.load(file)

camera = cv2.VideoCapture(0)

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

while True:

    ret, frame = camera.read()

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_detector.detectMultiScale(
        gray,
        1.2,
        5
    )

    for (x,y,w,h) in faces:

        face = gray[y:y+h,x:x+w]

        face = cv2.resize(
            face,
            (100,100)
        )

        vector = face.flatten()

        best_name = "Unknown"

        best_score = 999999999

        for person in database:

            for sample in database[person]:

                score = np.linalg.norm(
                    vector -
                    sample
                )

                if score < best_score:

                    best_score = score
                    best_name = person

        if best_score > 2500:

            best_name = "Unknown"

        cv2.rectangle(
            frame,
            (x,y),
            (x+w,y+h),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"{best_name}",
            (x,y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    cv2.imshow(
        "Modern Recognition",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

camera.release()

cv2.destroyAllWindows()
