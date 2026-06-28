import os
import time
import cv2
import subprocess

from flask import (
    Flask,
    Response,
    jsonify,
    send_file
)

app = Flask(__name__)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

LOG_FILE = os.path.join(
    BASE_DIR,
    "intrusion_log.txt"
)

SNAPSHOT_DIR = os.path.join(
    BASE_DIR,
    "snapshots"
)

camera = cv2.VideoCapture(0)

camera.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    640
)

camera.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    480
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

@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype=
        "multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/stats")
def stats():

    try:

        with open(
            LOG_FILE,
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

    if os.path.exists(SNAPSHOT_DIR):

        images = sorted(
            os.listdir(SNAPSHOT_DIR),
            key=lambda x:
            os.path.getmtime(
                os.path.join(
                    SNAPSHOT_DIR,
                    x
                )
            )
        )

        if images:

            latest_image = images[-1]

    return jsonify({
        "count": intrusion_count,
        "event": last_event,
        "image": latest_image,
        "history": logs[-10:]
    })

@app.route("/")
def home():

    subprocess.run(
        ["python3", "generate_chart.py"]
    )

    try:

        with open(
            LOG_FILE,
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

    gallery_html = ""

    if os.path.exists(SNAPSHOT_DIR):

        images = sorted(
            os.listdir(SNAPSHOT_DIR),
            key=lambda x:
            os.path.getmtime(
                os.path.join(
                    SNAPSHOT_DIR,
                    x
                )
            ),
            reverse=True
        )[:5]

        for image in images:

            gallery_html += f"""
            <img
            src="/snapshot/{image}?t={time.time()}"
            width="220"
            style="
            margin:10px;
            border-radius:10px;
            ">
            """

        gallery_html = f"""
        <div class="card">
        <h2>📸 Intruder Gallery</h2>
        {gallery_html}
        </div>
        """

    return f"""
<!DOCTYPE html>
<html>
<head>

<title>SentinelAI Dashboard</title>

<style>

body {{
background:#0f172a;
color:white;
font-family:Arial,sans-serif;
margin:20px;
}}

h1 {{
text-align:center;
}}

.card {{
background:#1e293b;
padding:20px;
border-radius:15px;
margin-bottom:20px;
box-shadow:0 0 15px rgba(0,0,0,0.3);
}}

.stat {{
font-size:40px;
font-weight:bold;
color:#38bdf8;
}}

img {{
border-radius:10px;
}}

.grid {{
display:grid;
grid-template-columns:
repeat(3,1fr);
gap:20px;
}}

.small-card {{
background:#1e293b;
padding:20px;
border-radius:15px;
text-align:center;
box-shadow:0 0 15px rgba(0,0,0,0.3);
}}

pre {{
color:white;
}}

.status-dot{{
width:30px;
height:30px;
background:#00ff00;
border-radius:50%;
margin:auto;
box-shadow:
0 0 10px #00ff00,
0 0 20px #00ff00,
0 0 30px #00ff00;
}}

</style>

</head>

<body>

<h1>🛡️ SentinelAI Security Center</h1>

<div class="grid">

<div class="small-card">

<h3>Total Intrusions</h3>

<div
class="stat"
id="count">

{intrusion_count}

</div>

</div>

<div class="small-card">

<h3>Status</h3>

<div class="stat">

<div class="status-dot"></div>

</div>

</div>

<div class="small-card">

<h3>Last Event</h3>

<div>

{last_event}

</div>

</div>

</div>

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

{gallery_html}

<div class="card">

<h2>Latest Event</h2>

<pre id="event">

{last_event}

</pre>

</div>

<div class="card">

<h2>📊 Intrusion Analytics</h2>

<img
src="/chart?t={time.time()}"
width="700">

</div>

<div class="card">

<h2>📜 Intrusion History</h2>

<pre id="history">

{"".join(logs[-10:])}

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

document.getElementById(
"history"
).innerText =
data.history.join("");

location.reload();

}});

}}, 5000);

</script>

</body>

</html>
"""

@app.route("/snapshot/<filename>")
def snapshot(filename):

    image_path = os.path.join(
        SNAPSHOT_DIR,
        filename
    )

    return send_file(
        image_path
    )

@app.route("/chart")
def chart():

    return send_file(
        "chart.png"
    )

if __name__ == "__main__":

    app.run(
        debug=False,
        port=5050
    )