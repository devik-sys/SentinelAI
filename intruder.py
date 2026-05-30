from datetime import datetime
import cv2
import time
import os

# ----------------------------
# CREATE FOLDERS
# ----------------------------

os.makedirs("recordings", exist_ok=True)
os.makedirs("snapshots", exist_ok=True)

# ----------------------------
# FACE DETECTOR
# ----------------------------

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# ----------------------------
# CAMERA
# ----------------------------

cam = cv2.VideoCapture(0)

frame_width = 640
frame_height = 480

cam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# ----------------------------
# VIDEO WRITER
# ----------------------------

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

video_name = f"recordings/intruder_{int(time.time())}.mov"

out = cv2.VideoWriter(
    video_name,
    fourcc,
    20.0,
    (frame_width, frame_height)
)

# ----------------------------
# MOTION VARIABLES
# ----------------------------

ret, frame1 = cam.read()
ret, frame2 = cam.read()

recording = False
snapshot_taken = False

# ----------------------------
# MAIN LOOP
# ----------------------------

while cam.isOpened():

    diff = cv2.absdiff(frame1, frame2)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    _, thresh = cv2.threshold(
        blur,
        20,
        255,
        cv2.THRESH_BINARY
    )

    dilated = cv2.dilate(
        thresh,
        None,
        iterations=3
    )

    contours, _ = cv2.findContours(
        dilated,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    motion_detected = False

    for contour in contours:

        if cv2.contourArea(contour) < 2000:
            continue

        motion_detected = True

    # ----------------------------
    # FACE DETECTION
    # ----------------------------

    gray_frame = cv2.cvtColor(
        frame1,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray_frame,
        1.1,
        4
    )

    # ----------------------------
    # MOTION + FACE REQUIRED
    # ----------------------------

    if motion_detected and len(faces) > 0:

        recording = True

        status = "RECORDING"
        color = (0, 0, 255)

        if not snapshot_taken:

            snapshot_name = (
                f"snapshots/intruder_{int(time.time())}.jpg"
            )

            cv2.imwrite(
                snapshot_name,
                frame1
            )

            print(
                "Snapshot Saved:",
                snapshot_name
            )

            snapshot_taken = True

    else:

        recording = False
        snapshot_taken = False

        status = "MONITORING"
        color = (0, 255, 0)

    # ----------------------------
    # DRAW FACE BOXES
    # ----------------------------

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame1,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    # ----------------------------
    # CCTV OVERLAY
    # ----------------------------

    cv2.putText(
        frame1,
        status,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cv2.putText(
        frame1,
        f"Faces: {len(faces)}",
        (10, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cv2.putText(
        frame1,
        current_time,
        (10, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # ----------------------------
    # RECORD VIDEO
    # ----------------------------

    if recording:
        out.write(frame1)

    # ----------------------------
    # SHOW WINDOW
    # ----------------------------

    cv2.imshow(
        "SentinelAI Surveillance",
        frame1
    )

    frame1 = frame2
    ret, frame2 = cam.read()

    if not ret:
        break

    if cv2.waitKey(1) == ord('q'):
        break

# ----------------------------
# CLEANUP
# ----------------------------

cam.release()
out.release()
cv2.destroyAllWindows()