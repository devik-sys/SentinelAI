from deepface import DeepFace
import os


def recognize(frame):

    try:

        result = DeepFace.find(
            img_path=frame,
            db_path="faces",
            model_name="Facenet",
            enforce_detection=False,
            silent=True
        )

        if len(result) > 0 and len(result[0]) > 0:

            identity = result[0].iloc[0]["identity"]

            name = os.path.basename(
                os.path.dirname(identity)
            )

            return name

        return "Unknown"

    except Exception as e:

        print("Recognition Error:", e)
        return "Unknown"