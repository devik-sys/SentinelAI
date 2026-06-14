# SentinelAI

AI-Powered Smart Surveillance System

## Features

* Motion Detection using OpenCV
* Face Detection using Haar Cascade
* Face Recognition using LBPH Recognizer
* Authorized User Access Control
* Intruder Detection
* Snapshot Capture
* Automatic Video Recording
* Email Alert System
* Intrusion Logging

## Tech Stack

* Python
* OpenCV
* LBPH Face Recognition
* SMTP Email Alerts
* NumPy

## Project Workflow

1. Camera monitors surroundings
2. Motion is detected
3. Face is detected
4. Face Recognition verifies identity

### Known User

* Access Granted
* No alert generated

### Unknown User

* Snapshot captured
* Video recording started
* Email alert sent
* Intrusion logged

## Folder Structure

EdgeAI/
├── face_recognition.py
├── recognize_face.py
├── collect_faces.py
├── train_model.py
├── trainer.yml
├── snapshots/
├── recordings/
├── logs/
├── known_faces/
└── README.md

## Future Improvements

* DeepFace Integration
* Real-Time Dashboard
* Cloud Storage
* Mobile Notifications
* Multi-User Recognition

## Author

Devi Krishna Manoj

Electronics and Communication Engineering Student

Building AI, Computer Vision and Edge AI Projects