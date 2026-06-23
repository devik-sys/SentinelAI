import cv2
import os
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []

people = {
    "devi": 0,
    "mama": 1,
    "dada": 2
}

for person_name, label in people.items():

    person_path = os.path.join(
        "faces",
        person_name
    )

    if not os.path.exists(person_path):
        continue

    for image_name in os.listdir(person_path):

        image_path = os.path.join(
            person_path,
            image_name
        )

        img = cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE
        )

        if img is None:
            continue

        img = cv2.resize(
            img,
            (200, 200)
        )

        faces.append(img)
        labels.append(label)

print(
    f"Training on {len(faces)} images"
)

recognizer.train(
    faces,
    np.array(labels)
)

recognizer.save(
    "trainer.yml"
)

print(
    "Multi-user model trained!"
)