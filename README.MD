# 🎓 Face Recognition Based Attendance System

## Introduction

Attendance Management keeps track of your employee or students present/absent details. It is the system to document the time your employees/students work and the time they take off.

 In this digital era, face recognition system plays a vital role in  almost every  sector. Face recognition  is one  of the mostly used biometrics. It can used for security, authentication, identification.

This is an artificial intelligence based attendance management system with face recognition technology. The main objective of this AI based software solution is to update attendance with employees' face using computer vision.

This project can be divided into two main sub-systems. Attendance receiver module also called as face scanner (Written in Python) for reading and updating attendance to the database, and management module (Written in C#) for creating datasets of employees, training AI models with GUI, entering employees details and other management relented operations .



> An AI-powered automated attendance system using real-time face recognition and QR code verification, built as a Final Year Project at NRI Institute of Technology.
> Deployed live on the web.

🔗 **Live API:** https://face-recognition-attendance-system-rp21.onrender.com


## 📌 Project Overview

This system automates student attendance using:
- **Face Recognition** — identifies students via webcam using dlib and face_recognition
- **QR Code Verification** — students scan a QR code before face verification
- **Eye Blink Detection** — prevents spoofing using photos (liveness detection)
- **Text-to-Speech** — voice confirmation when attendance is marked
- **MySQL Database** — stores all student data and attendance records
- **C# Management Panel** — GUI for administrators to manage students and view reports

---

## 👥 Team Members

| Name | Role |
|---|---|
| Galla Indranag | Team Lead & Backend Developer |
| Allu Lakshmi Triveni | Database & Testing |
| Bolla Nikitha Sai | Frontend & UI |
| Avancha Karthikbhat | Integration & Documentation |

**Institution:** NRI Institute of Technology, Guntur, Andhra Pradesh  
**Guide:** Mrs. Sujatha  
**Year:** 2024  
**Department:** Electronics & Communication Engineering

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.6 |
| Face Recognition | dlib 19.23.0, face_recognition 1.3.0 |
| Computer Vision | OpenCV 4.5.5 |
| Database | MySQL 8.0 |
| Management Panel | C# (.NET Framework) |
| QR Code | qrcode, pyzbar |
| Text-to-Speech | pyttsx3 |
| Eye Blink Detection | dlib facial landmarks + scipy |

---

## 📁 Project Structure

```
face-recognition-based-attendance-system-main/
│
├── 0-management-auto-attendance-system/   # C# Management Panel (Visual Studio)
│   └── Management_Auto_Attendance_System/
│       └── bin/Debug/
│           ├── run.py
│           ├── training.py
│           └── dataset-creator.py
│
├── 1-database/                            # MySQL database schema
│   └── management_auto_attendance_system.sql
│
├── 2-python-scripts/                      # Main Python scripts
│   ├── run.py                             # Main face recognition scanner
│   ├── training.py                        # Face model trainer
│   ├── dataset-creator.py                 # Student photo capture
│   ├── Shape_Model/                       # dlib landmark model (add manually)
│   ├── Cache/                             # Temporary face encodings
│   ├── Trained_Models/                    # Trained face recognition models
│   ├── Attendance_Pending_Images/         # Pending attendance snapshots
│   ├── AttendanceSystemData/              # Sound files
│   └── System_Settings/                  # System configuration
│
├── environment.yml                        # Conda environment definition
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Windows 10/11 (Windows only — uses Windows APIs)
- Anaconda
- Visual Studio 2022 with **Desktop development with C++** workload
- MySQL Server 8.0

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/indra675/face-recognition-based-attendance-system.git
cd face-recognition-based-attendance-system
```

---

### Step 2: Create Conda Environment

Open **Anaconda Prompt** and run:

```bash
conda create -n ai_attendance_system_env python=3.6
conda activate ai_attendance_system_env
```

---

### Step 3: Install Dependencies (in order)

```bash
pip install cmake==3.22.2
pip install dlib==19.23.0
pip install face_recognition==1.3.0
pip install opencv-python==4.5.5.62
pip install imutils==0.5.4
pip install pyttsx3==2.90
pip install playsound==1.2.2
pip install mysql-connector-python==8.0.28
pip install qrcode==7.3.1
pip install pyzbar==0.1.8
pip install scipy==1.5.4
pip install numpy==1.19.5
pip install pillow==8.4.0
pip install pywin32==303
```

> ⚠️ **dlib requires Microsoft C++ Build Tools.** Install from [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) with the **Desktop development with C++** workload before installing dlib.

---

### Step 4: Setup MySQL Database

1. Start MySQL Server
2. Open MySQL Workbench or Anaconda Prompt
3. Create the database:

```sql
CREATE DATABASE management_auto_attendance_system;
```

4. Import the schema:

```bash
cd 1-database
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p management_auto_attendance_system < management_auto_attendance_system.sql
```

---

### Step 5: Download Shape Predictor Model

Download the dlib facial landmark model (not included in repo due to size):

👉 [shape_predictor_68_face_landmarks.dat.bz2](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)

Extract and place it at:
```
2-python-scripts/Shape_Model/shape_predictor_68_face_landmarks.dat
```

---

### Step 6: Create Required Folders

Inside `2-python-scripts/`, create:

```bash
mkdir Shape_Model
mkdir Cache
mkdir Trained_Models
mkdir Attendance_Pending_Images
mkdir AttendanceSystemData
mkdir System_Settings
```

Add two MP3 sound files inside `AttendanceSystemData/`:
- `QRSound.mp3`
- `blinkSound.mp3`

Create `System_Settings/Face_rec.txt` with content:
```
True
```

---

### Step 7: Configure Database Credentials

Open `2-python-scripts/run.py` and update:

```python
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="your_mysql_password",
    database="management_auto_attendance_system"
)
```

---

## 🚀 Running the Project

### Start the Face Recognition Scanner

```bash
conda activate ai_attendance_system_env
cd "2-python-scripts"
python run.py
```

### Start the Management Panel

Open `0-management-auto-attendance-system/Management_Auto_Attendance_System.sln` in Visual Studio and press **F5**.

### Workflow

```
1. Admin adds student via Management Panel
2. Dataset Creator captures student photos
3. Training script trains the face model
4. QR codes generated for each student
5. Student scans QR code at attendance terminal
6. Face recognized + eye blink verified
7. Attendance marked in MySQL database
```

---

## 🔧 Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: dlib` | C++ Build Tools missing | Install Visual Studio C++ Build Tools |
| `Access denied for user root` | Wrong MySQL password in run.py | Update `passwd=` in run.py |
| `Unable to open shape_predictor_68_face_landmarks.dat` | Model file missing or corrupted | Re-download from dlib.net (must be 99,693,937 bytes) |
| `mysql not recognized` | MySQL not in PATH | Use full path: `C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe` |
| Camera not opening | Wrong camera index | Change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` |

---

## 📸 How It Works

1. **QR Code Scan** — Student presents QR code to camera
2. **Face Detection** — dlib detects face in real time
3. **Eye Blink Check** — Facial landmarks verify liveness (prevents photo spoofing)
4. **Face Recognition** — Compares face encoding against trained models
5. **Attendance Marked** — Record saved to MySQL with timestamp
6. **Voice Confirmation** — pyttsx3 announces student name

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [face_recognition library](https://github.com/ageitgey/face_recognition) by Adam Geitgey
- [dlib](http://dlib.net/) by Davis King
- Mrs. Sujatha — Project Guide, NRI Institute of Technology
- Department of ECE, NRI Institute of Technology, Guntur

---

<p align="center">Made with ❤️ by Team | NRI Institute of Technology | 2024</p>

---

## Social Links

* [Linkedin Profile](https://www.LinkedIn.com/in/gallaindranag)
