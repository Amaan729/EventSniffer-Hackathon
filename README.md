# EventSniffer ⚡️
> From screen to schedule, instantly.

[![Made-with-Swift](httpshttps://img.shields.io/badge/Made%20with-Swift-F05138.svg?style=for-the-badge&logo=swift)](https://www.swift.org)
[![Made-with-Python](https://img.shields.io/badge/Made%20with-Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Powered-by-spaCy](https://img.shields.io/badge/Powered%20by-spaCy-09A3D5.svg?style=for-the-badge&logo=spacy&logoColor=white)](https://spacy.io)
[![Built-with-Flask](https://img.shields.io/badge/Built%20with-Flask-000000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)

---

## 🚀 The Demo
**[➡️ Watch the 2-Minute Demo Video Here](https://youtu.be/U0LHpKopZn4)**

*Because this project involves complex local permissions (Accessibility, Calendar) and a local AI model, a live install is impractical for judging. This video shows the complete, end-to-end functionality.*

---

## 💡 The Problem
We're constantly scheduling. Events, meetings, and plans are buried in Slack messages, emails, and personal notes. Every time, we're forced to stop, open our calendar, and manually copy-and-paste the details. This is a small, constant, and universal friction point.

## ✨ The Solution
**EventSniffer** is an intelligent macOS assistant that automates this entire process.

It's a native menu bar app that "watches" the text in your *currently active window*. When it detects a potential event (like "sync tomorrow at 10am on Zoom"), it sends a native macOS notification. With one click on the "Add to Calendar" button, the event is instantly saved to your Apple Calendar—no typing, no copying, no context-switching.

---

## ⚙️ Architecture: 100% Local and Private
This project runs entirely on your machine. Your text never leaves your laptop. It consists of two components that communicate locally:

* **`app/` (The "Body"):** A native Swift & SwiftUI app that lives in the macOS menu bar. It uses the **Accessibility API** to "surgically" read text from the user's focused UI element (like a text field) and **EventKit** to create calendar events.
* **`ml/` (The "Brain"):** A local Python server. It runs a **custom-trained spaCy NER model** wrapped in a **Flask API**. The Swift app sends all text to this local server for analysis.

**The Data Flow:**
`[Swift App]` → `(Reads active text)` → `[POST to http://127.0.0.1:5000]` → `[Python/Flask Server]` → `[spaCy NER Model]` → `(Finds EVENT, DATE, TIME)` → `[JSON Response]` → `[Swift App]` → `[macOS Notification]` → `[User clicks 'Add']` → `[EventKit adds to Calendar]`

---

## 🛠️ How to Run (For Developers)
This project requires running two separate processes: the Python server and the Swift app.

### 1. Run the "Brain" (Python ML Server)
First, get the AI model and API server running.

```bash
# 1. Navigate to the ml folder
cd ml

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install all dependencies from the requirements file
pip install -r requirements.txt

# 4. Run the Flask server!
python server.py
