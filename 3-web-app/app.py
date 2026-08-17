import os
import sqlite3
import pickle
import base64
from datetime import datetime, date
from io import BytesIO

import numpy as np
import face_recognition
from PIL import Image
from flask import Flask, render_template, request, jsonify, redirect, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")
FACES_DIR = os.path.join(BASE_DIR, "known_faces")
ENCODINGS_PATH = os.path.join(BASE_DIR, "encodings.pickle")

os.makedirs(FACES_DIR, exist_ok=True)

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )"""
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Face encoding storage (pickle file: {emp_id: {"name": str, "encodings": [np.array,...]}})
# ---------------------------------------------------------------------------
def load_encodings():
    if os.path.exists(ENCODINGS_PATH):
        with open(ENCODINGS_PATH, "rb") as f:
            return pickle.load(f)
    return {}


def save_encodings(data):
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(data, f)


def decode_image(data_url):
    """Decode a base64 data URL (from <canvas>.toDataURL()) into an RGB numpy array."""
    header, encoded = data_url.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    return np.array(img)


# ---------------------------------------------------------------------------
# Routes - pages
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/enroll")
def enroll_page():
    return render_template("enroll.html")


@app.route("/attendance")
def attendance_page():
    return render_template("attendance.html")


@app.route("/log")
def log_page():
    conn = get_db()
    today = date.today().isoformat()
    rows = conn.execute(
        "SELECT * FROM attendance WHERE date = ? ORDER BY timestamp DESC", (today,)
    ).fetchall()
    conn.close()
    return render_template("log.html", rows=rows, today=today)


# ---------------------------------------------------------------------------
# Routes - API
# ---------------------------------------------------------------------------
@app.route("/api/employees")
def api_employees():
    conn = get_db()
    rows = conn.execute("SELECT emp_id, name FROM employees ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/enroll", methods=["POST"])
def api_enroll():
    """Register a new employee using several captured face frames."""
    payload = request.get_json(force=True)
    emp_id = (payload.get("emp_id") or "").strip()
    name = (payload.get("name") or "").strip()
    frames = payload.get("frames") or []

    if not emp_id or not name:
        return jsonify({"ok": False, "error": "Employee ID and name are required."}), 400
    if len(frames) < 3:
        return jsonify({"ok": False, "error": "Please capture at least 3 photos."}), 400

    encodings = []
    for frame in frames:
        try:
            img = decode_image(frame)
        except Exception:
            continue
        boxes = face_recognition.face_locations(img, model="hog")
        if len(boxes) != 1:
            continue  # skip frames with no face or more than one face
        enc = face_recognition.face_encodings(img, boxes)[0]
        encodings.append(enc)

    if len(encodings) < 2:
        return jsonify({
            "ok": False,
            "error": "Couldn't get clear single-face shots. Make sure only your face is visible, well lit, and try again."
        }), 400

    data = load_encodings()
    data[emp_id] = {"name": name, "encodings": encodings}
    save_encodings(data)

    conn = get_db()
    conn.execute(
        "INSERT OR REPLACE INTO employees (emp_id, name, created_at) VALUES (?, ?, ?)",
        (emp_id, name, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()

    return jsonify({"ok": True, "captured": len(encodings)})


@app.route("/api/mark_attendance", methods=["POST"])
def api_mark_attendance():
    """Take a single webcam frame, match against known faces, log attendance."""
    payload = request.get_json(force=True)
    frame = payload.get("frame")
    if not frame:
        return jsonify({"ok": False, "error": "No frame received."}), 400

    try:
        img = decode_image(frame)
    except Exception:
        return jsonify({"ok": False, "error": "Could not read image."}), 400

    boxes = face_recognition.face_locations(img, model="hog")
    if not boxes:
        return jsonify({"ok": False, "error": "No face detected. Face the camera and try again."})

    encodings = face_recognition.face_encodings(img, boxes)
    known = load_encodings()

    if not known:
        return jsonify({"ok": False, "error": "No employees enrolled yet."})

    known_ids = []
    known_names = []
    known_vecs = []
    for emp_id, rec in known.items():
        for enc in rec["encodings"]:
            known_ids.append(emp_id)
            known_names.append(rec["name"])
            known_vecs.append(enc)
    known_vecs = np.array(known_vecs)

    results = []
    now = datetime.now()
    today = now.date().isoformat()

    conn = get_db()
    for face_enc in encodings:
        dists = face_recognition.face_distance(known_vecs, face_enc)
        best_idx = int(np.argmin(dists))
        best_dist = float(dists[best_idx])

        THRESHOLD = 0.5
        if best_dist > THRESHOLD:
            results.append({"status": "unknown", "distance": round(best_dist, 3)})
            continue

        emp_id = known_ids[best_idx]
        name = known_names[best_idx]

        already = conn.execute(
            "SELECT 1 FROM attendance WHERE emp_id = ? AND date = ?", (emp_id, today)
        ).fetchone()

        if already:
            results.append({"status": "already_marked", "emp_id": emp_id, "name": name})
        else:
            conn.execute(
                "INSERT INTO attendance (emp_id, name, date, time, timestamp) VALUES (?, ?, ?, ?, ?)",
                (emp_id, name, today, now.strftime("%H:%M:%S"), now.isoformat()),
            )
            conn.commit()
            results.append({
                "status": "marked",
                "emp_id": emp_id,
                "name": name,
                "time": now.strftime("%H:%M:%S"),
                "distance": round(best_dist, 3),
            })

    conn.close()
    return jsonify({"ok": True, "results": results})

init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
