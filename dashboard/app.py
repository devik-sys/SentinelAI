import os
import time
import cv2

from flask import (
    Flask,
    Response,
    jsonify,
    send_file
)

app = Flask(__name__)

print(os.getcwd())

# -----------------------------
# Camera
# -----------------------------

camera = cv2.VideoCapture(0)

camera.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    640
)

camera.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    480
)

print(
    "Camera Open:",
    camera.isOpened()
)


def generate_frames():

    while True:

        success, frame = camera.read()

        if not success:
            break

        _, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )


# -----------------------------
# Live Camera Feed
# -----------------------------

@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype=
        "multipart/x-mixed-replace; boundary=frame"
    )


# -----------------------------
# Dashboard API
# -----------------------------

@app.route("/stats")
def stats():

    try:

        with open(
            "intrusion_log.txt",
            "r"
        ) as file:

            logs = file.readlines()

    except:

        logs = []

    intrusion_count = len(logs)

    last_event = (
        logs[-1]
        if logs
        else "No Events"
    )

    latest_image = ""

    if os.path.exists("snapshots"):

        images = sorted(
            os.listdir("snapshots"),
            key=lambda x:
            os.path.getmtime(
                os.path.join(
                    "snapshots",
                    x
                )
            )
        )

        if images:

            latest_image = images[-1]

    return jsonify({
        "count": intrusion_count,
        "event": last_event,
        "image": latest_image
    })


# -----------------------------
# Dashboard
# -----------------------------

@app.route("/")
def home():

    try:

        with open(
            "intrusion_log.txt",
            "r"
        ) as file:

            logs = file.readlines()

    except:

        logs = []

    intrusion_count = len(logs)

    last_event = (
        logs[-1]
        if logs
        else "No Events"
    )

    latest_image = ""

    if os.path.exists("snapshots"):

        images = sorted(
            os.listdir("snapshots"),
            key=lambda x:
            os.path.getmtime(
                os.path.join(
                    "snapshots",
                    x
                )
            )
        )

        if images:

            latest_image = images[-1]

    image_html = ""

    if latest_image:

        image_html = f"""
        <div class="card">
        <h2>📸 Latest Snapshot</h2>

        <img
        id="snapshot"
        src="/snapshot/{latest_image}?t={time.time()}"
        width="500">

        </div>
        """

    return f"""
<!DOCTYPE html>

<html>

<head>

<title>SentinelAI Dashboard</title>

<style>

body {{
    font-family: Arial;
    background: #f4f6f9;
    margin: 40px;
}}

.card {{
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}}

.stat {{
    font-size: 30px;
    font-weight: bold;
}}

img {{
    border-radius: 10px;
}}

</style>

</head>

<body>

<h1>🛡️ SentinelAI Dashboard</h1>

<div class="card">

<h2>Total Intrusions</h2>

<div
class="stat"
id="count">

{intrusion_count}

</div>

</div>

<div class="card">

<h2>🎥 Live Camera Feed</h2>

<img
src="/video_feed"
width="700">

</div>

<div class="card">

<h2>System Status</h2>

<div class="stat">

🟢 Active

</div>

</div>

{image_html}

<div class="card">

<h2>Latest Event</h2>

<pre id="event">

{last_event}

</pre>

</div>

<script>

setInterval(() => {{

fetch("/stats")
.then(response => response.json())
.then(data => {{

document.getElementById(
"count"
).innerText = data.count;

document.getElementById(
"event"
).innerText = data.event;

if(data.image) {{

document.getElementById(
"snapshot"
).src =
"/snapshot/" +
data.image +
"?t=" +
Date.now();

}}

}});

}}, 5000);

</script>

</body>

</html>
"""


# -----------------------------
# Snapshot Route
# -----------------------------

@app.route("/snapshot/<filename>")
def snapshot(filename):

    image_path = os.path.join(
        os.getcwd(),
        "snapshots",
        filename
    )

    return send_file(
        image_path
    )


# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":

    app.run(
        debug=False,
        port=5050
    )