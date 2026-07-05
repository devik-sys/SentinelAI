from deepface import DeepFace
import cv2
import os

camera = cv2.VideoCapture(0)

print("Starting AI Face Recognition...")

while True:

    ret, frame = camera.read()

    if not ret:
        break

    try:

        result = DeepFace.find(
            img_path=frame,
            db_path="faces",
            model_name="Facenet",
            enforce_detection=False,
            silent=True
        )

        # Debug: print the result
        print(result)

        if len(result) > 0 and len(result[0]) > 0:

            if len(result) > 0 and len(result[0]) > 0:

                best = result[0].iloc[0]

                distance = best["distance"]

                identity = best["identity"]

                name = identity.split("/")[1]

                if distance < 0.35:

                    cv2.putText(
                        frame,
                        name,
                        (40,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,255,0),
                        2
                    )

                    print("Recognized:", name)

                else:

                    cv2.putText(
                        frame,
                        "Unknown",
                        (40,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,0,255),
                        2
                    )

            else:

                cv2.putText(
                    frame,
                    "Unknown",
                    (40,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    2
                )

            cv2.putText(
                frame,
                name,
                (40, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        else:

            cv2.putText(
                frame,
                "Unknown",
                (40, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

    except Exception as e:

        print("ERROR:", e)

        cv2.putText(
            frame,
            "Unknown",
            (40, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    cv2.imshow(
        "SentinelAI DeepFace",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()