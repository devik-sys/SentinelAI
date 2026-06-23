import cv2
import os
import numpy as np

data_path = "faces/devi"

faces = []
labels = []

for image_name in os.listdir(data_path):

    image_path = os.path.join(
        data_path,
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

    labels.append(0)

print(
    f"Training on {len(faces)} images"
)

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.train(
    faces,
    np.array(labels)
)

recognizer.save(
    "trainer.yml"
)

print(
    "Model Trained Successfully!"
)
