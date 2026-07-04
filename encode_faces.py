import os
import pickle
import cv2

KNOWN_FACES_DIR = "faces"

encodings = {}
names = []

for person in os.listdir(KNOWN_FACES_DIR):

    person_path = os.path.join(
        KNOWN_FACES_DIR,
        person
    )

    if not os.path.isdir(person_path):
        continue

    names.append(person)

    encodings[person] = []

    for image_name in os.listdir(person_path):

        image_path = os.path.join(
            person_path,
            image_name
        )

        image = cv2.imread(image_path)

        if image is None:
            continue

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        resized = cv2.resize(
            gray,
            (100,100)
        )

        encodings[person].append(
            resized.flatten()
        )

with open(
    "face_encodings.pkl",
    "wb"
) as file:

    pickle.dump(
        encodings,
        file
    )

print(
    "Face database created successfully!"
)
