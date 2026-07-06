import cv2

from camera import get_frame, release_camera
from ai_recognition import recognize

while True:

    frame = get_frame()

    if frame is None:
        break

    # AI Recognition
    name = recognize(frame)

    # Display Name
    cv2.putText(
        frame,
        name,
        (40, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("SentinelAI Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

release_camera()
cv2.destroyAllWindows()