# Face Recognition Attendance — Web App

A browser-based version of the original desktop project: enroll faces via
webcam, mark attendance with face recognition, and view today's log — all
in a web UI running locally (Flask + SQLite instead of C#/WinForms + MySQL).

## Setup (Windows)

1. Install Python 3.9–3.11.
2. Open a terminal in this folder.
3. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate

4. Install dependencies:

pip install cmake
pip install dlib
pip install -r requirements.txt
pip install "setuptools<81"

5. Run the app:

python app.py

6. Open `http://127.0.0.1:5000` in your browser.

## Using it

1. **Enroll** — enter Employee ID + Name, start the camera, capture 3–5
   clear photos, save.
2. **Mark Attendance** — start the camera, click "Scan & Mark Attendance".
3. **Today's Log** — view everyone marked present today.

Data is stored locally in `attendance.db` (SQLite) and `encodings.pickle`
(face encodings), both created automatically on first run.