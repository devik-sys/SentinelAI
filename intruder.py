from datetime import datetime
import cv2
import time
import os

import smtplib
from email.message import EmailMessage

# ----------------------------
# CREATE FOLDERS
# ----------------------------

os.makedirs("recordings", exist_ok=True)
os.makedirs("snapshots", exist_ok=True)

os.makedirs("logs", exist_ok=True)

# ----------------------------
# EMAIL SETTINGS
# ----------------------------

EMAIL_ADDRESS = "YOUR_EMAIL"
EMAIL_PASSWORD = "YOUR_APP_PASSWORD"

last_email_time = 0
EMAIL_COOLDOWN = 60

def send_email_alert(snapshot_path):

    try:

        msg = EmailMessage()

        msg["Subject"] = "🚨 SentinelAI Alert"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        msg.set_content(
            f"""
🚨 SENTINELAI ALERT 🚨

Motion and face detected.

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Action Taken:
✅ Snapshot Captured
✅ Video Recording Started
✅ Email Alert Sent

Check SentinelAI recordings and snapshots.
"""
        )

        with open(snapshot_path, "rb") as image_file:

            image_data = image_file.read()

            image_name = os.path.basename(snapshot_path)

            msg.add_attachment(
                image_data,
                maintype="image",
                subtype="jpeg",
                filename=image_name
            )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            smtp.send_message(msg)

        print("📧 Email Alert Sent!")

    except Exception as e:

        print("Email Error:", e)

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            smtp.send_message(msg)

        print("📧 Email Alert Sent!")

    except Exception as e:

        print("Email Error:", e)

def write_log(message):

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        "logs/events.txt",
        "a"
    ) as log_file:

        log_file.write(
            f"{current_time} | {message}\n"
        )

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

recording_start_time = 0
RECORD_DURATION = 15

intrusion_count = 0

# ----------------------------
# MAIN LOOP
# ----------------------------

while cam.isOpened():

    current_time = time.time()

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

        if recording_start_time == 0:

            recording_start_time = time.time()
            
            intrusion_count += 1

            write_log(
                f"Recording Started | Intrusion #{intrusion_count}"
            )

            print(
                "Recording Started"
            )

        # write_log("Motion + Face Detected")

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

            write_log("Snapshot Saved")

            snapshot_taken = True

            current_time = time.time()

            if (
                current_time - last_email_time
                > EMAIL_COOLDOWN
            ):

                send_email_alert(snapshot_name)

                write_log("Email Alert Sent")

                last_email_time = current_time

    else:

        if recording_start_time == 0:

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

    cv2.putText(
        frame1,
        f"Intrusions: {intrusion_count}",
        (10, 140),
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

        if (
            time.time() - recording_start_time
            > RECORD_DURATION
        ):

            recording = False

            recording_start_time = 0

            snapshot_taken = False

            write_log("Recording Stopped")

            print("Recording Stopped")
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
