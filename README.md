# 🛡️ SentinelAI

### AI-Powered Smart Surveillance System using OpenCV & Edge AI

An intelligent surveillance system that detects motion, recognizes authorized users, identifies intruders, records evidence, and sends real-time email alerts.

---

## 📸 Project Preview

### Monitoring Mode

![Monitoring](screenshots/monitoring.png)

### Intruder Detection & Recording

![Recording](screenshots/recording.png)

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

## ⚙️ System Workflow

text
Camera Feed
     ↓
Motion Detection
     ↓
Face Detection
     ↓
Face Recognition
     ↓
 ┌───────────────┬───────────────┐
 │ Known User    │ Unknown User  │
 └───────────────┴───────────────┘
         ↓                 ↓
 Access Granted    Intruder Alert
                   Snapshot Saved
                   Recording Started
                   Email Sent
                   Event Logged


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

text
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
│   ├── monitoring.png
│   └── recording.png
└── README.md

---

## 🔮 Future Improvements

* DeepFace Integration
* Multi-User Recognition
* Cloud Storage
* Mobile Notifications
* Real-Time Dashboard
* Web-Based Monitoring Panel

---

## 👨‍💻 Author

### Devi Krishna Manoj

ECE Student • Edge AI • Computer Vision • AI Automation

Building intelligent systems at the intersection of AI and embedded technologies.
