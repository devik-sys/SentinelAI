import cv2
import os

person_name = input("Enter name: ")

save_path = f"faces/{person_name}"

os.makedirs(save_path, exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

count = 0
frame_count = 0

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

        face = gray[
            y:y+h,
            x:x+w
        ]

        face = cv2.resize(
            face,
            (200, 200)
        )

        frame_count += 1

        if frame_count % 5 == 0:

            count += 1

            cv2.imwrite(
                f"{save_path}/{count}.jpg",
                face
            )

            print(
                f"Saved image {count}"
            )

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0,255,0),
            2
        )

    cv2.imshow(
        "Collect Faces",
        frame
    )

    if count >= 50:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(
    f"Collected {count} images."
)