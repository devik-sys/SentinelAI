import time
import cv2
from flask import Response
from flask import Flask
import os

app = Flask(__name__)
print(os.getcwd())

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Camera Open:", camera.isOpened())

def generate_frames():

    while True:

        print("Streaming frame")

        success, frame = camera.read()

        if not success:
            break

        else:

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
        'multipart/x-mixed-replace; boundary=frame'
    )

@app.route("/")
def home():

    try:
        with open("intrusion_log.txt", "r") as file:
            logs = file.readlines()
    except:
        logs = []

    intrusion_count = len(logs)

    last_event = logs[-1] if logs else "No Events"

    latest_image = ""

    if os.path.exists("snapshots"):

        images = sorted(
            os.listdir("snapshots"),
            key=lambda x: os.path.getmtime(
                os.path.join("snapshots", x)
            )
        )

        if images:

            latest_image = images[-1]

            print("Latest image:", latest_image)

    image_html = ""

    if latest_image:

        image_html = f"""
        <h3>Latest Snapshot</h3>
        <img src="/snapshot/{latest_image}?t={time.time()}"
        width="500">
        """

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

    <meta http-equiv="refresh" content="5">

    <title>SentinelAI Dashboard</title>

    <style>

    body {{
        font-family: Arial;
        background: #f4f6f9;
        margin: 40px;
    }}

    h1 {{
        color: #1e3a8a;
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

    <div class="stat">
    {intrusion_count}
    </div>

    </div>

    <div class="card">

    <h2>🎥 Live Camera Feed</h2>

    <img
    src="http://127.0.0.1:5050/video_feed"
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

    <pre>{last_event}</pre>

    </div>

    </body>

    </html>
"""

@app.route("/snapshot/<filename>")
def snapshot(filename):

    from flask import send_file
    import os

    image_path = os.path.join(
        os.getcwd(),
        "snapshots",
        filename
    )

    print("Loading:", image_path)

    return send_file(image_path)

if __name__ == "__main__":
    app.run(
        debug=False,
        port=5050
    )