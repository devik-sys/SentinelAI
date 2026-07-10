from deepface import DeepFace
import cv2
import os

MODELS = [
    "Facenet",
    "ArcFace",
    "GhostFaceNet",
    "SFace"
]

camera = cv2.VideoCapture(0)

print("\n===== SentinelAI Model Benchmark =====\n")

for model in MODELS:

    print(f"\nTesting {model}...\n")

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        result = DeepFace.find(
            img_path=frame,
            db_path="../faces",
            model_name=model,
            enforce_detection=False,
            silent=True
        )

        if len(result) > 0 and len(result[0]) > 0:

            best = result[0].iloc[0]

            identity = best["identity"]
            distance = best["distance"]
            confidence = best["confidence"]

            name = os.path.basename(os.path.dirname(identity))

            text = f"{model} | {name}"

            print(
                f"{model} -> {name} | Distance: {distance:.4f} | Confidence: {confidence:.2f}%"
            )

        else:

            text = f"{model} | Unknown"

            print(f"{model} -> Unknown")

        cv2.putText(
            frame,
            text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Model Test", frame)

        key = cv2.waitKey(1)

        if key == ord("n"):
            break

        if key == ord("q"):
            camera.release()
            cv2.destroyAllWindows()
            exit()

camera.release()
cv2.destroyAllWindows()
