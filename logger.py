import os
from datetime import datetime

LOG_FILE = "logs/events.log"

os.makedirs("logs", exist_ok=True)


def log_event(message):

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as file:
        file.write(f"[{now}] {message}\n")

    print(f"[{now}] {message}")
