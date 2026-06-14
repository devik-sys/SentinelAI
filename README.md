# 🛡️ SentinelAI

## AI-Powered Smart Surveillance System using OpenCV & Edge AI

An intelligent surveillance system that detects motion, recognizes authorized users, identifies intruders, records evidence, and sends real-time email alerts.

---

## 📸 Project Preview

### Monitoring Mode

![Monitoring](screenshots/monitoring_mode.png)

### Intruder Detection & Recording

![Recording](screenshots/recording_mode.png)

---

## 🚀 Features

* 🎯 Motion Detection
* 👤 Face Detection
* 🧠 LBPH Face Recognition
* ✅ Authorized User Verification
* 🚨 Intruder Detection
* 📸 Snapshot Capture
* 🎥 Automatic Video Recording
* 📧 Email Alerts
* 📝 Intrusion Logging

---

## ⚙️ How It Works

1. Camera continuously monitors surroundings
2. Motion is detected
3. Face is detected
4. Face Recognition verifies identity

### Known User

* Access Granted
* No Alert Generated
* No Recording Started

### Unknown User

* Intruder Alert Triggered
* Snapshot Captured
* Video Recording Started
* Email Alert Sent
* Event Logged

---

## 🛠️ Tech Stack

| Technology | Purpose          |
| ---------- | ---------------- |
| Python     | Core Development |
| OpenCV     | Computer Vision  |
| LBPH       | Face Recognition |
| SMTP       | Email Alerts     |
| NumPy      | Image Processing |

---

## 📂 Project Structure

```text
EdgeAI/
├── face_recognition.py
├── recognize_face.py
├── collect_faces.py
├── train_model.py
├── trainer.yml
├── snapshots/
├── recordings/
├── logs/
├── screenshots/
│   ├── monitoring_mode.png
│   └── recording_mode.png
└── README.md
```

---

## 🔮 Future Improvements

* DeepFace Integration
* Multi-User Recognition
* Cloud Storage Integration
* Mobile Notifications
* Real-Time Dashboard
* Web-Based Monitoring Panel

---

## 👨‍💻 Author

### Devi Krishna Manoj

ECE Student | Edge AI | Computer Vision | AI Automation

Building intelligent systems at the intersection of AI, Embedded Systems, and Computer Vision.

