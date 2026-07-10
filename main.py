import cv2

from camera import get_frame, release_camera
from ai_recognition import recognize

FRAME_SKIP = 15

frame_count = 0

last_name = "Unknown"

while True:

    frame = get_frame()

    if frame is None:
        break

    frame_count += 1

    # Run AI only every 15 frames
    if frame_count % FRAME_SKIP == 0:

        print("Running AI Recognition...")

        last_name = recognize(frame)

    # Display last recognized name
    color = (0, 255, 0)

    if last_name == "Unknown":
        color = (0, 0, 255)

    cv2.putText(
        frame,
        last_name,
        (40, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cv2.imshow("SentinelAI Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

release_camera()
cv2.destroyAllWindows()