from deepface import DeepFace
import cv2
import os

# Load OpenCV face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


def recognize(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(120,120)
    )

    # No face
    if len(faces) == 0:
        return "No Face"

    # Largest detected face
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])

    face = frame[y:y+h, x:x+w]

    try:

        result = DeepFace.find(
            img_path=face,
            db_path="faces",
            model_name="ArcFace",
            enforce_detection=False,
            silent=True
        )

        if len(result) > 0 and len(result[0]) > 0:

            best = result[0].iloc[0]

            identity = best["identity"]

            distance = best["distance"]

            print(f"Match: {identity}")
            print(f"Distance: {distance:.4f}")

            name = os.path.basename(
                os.path.dirname(identity)
            )

            if distance < 0.35:
                print("✅ Recognized:", name)
                return name

            print("❌ Unknown")
            return "Unknown"

        return "Unknown"

    except Exception:
        return "Unknown"