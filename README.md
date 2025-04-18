# ⚽ FootyMind: Player & Ball Tracking + Event Detection from Football Video

**FootyMind** is an AI-powered football analytics pipeline that tracks players and the ball, identifies team associations, and detects key match events like passes, tackles, and goals—all from match video footage. This project uses a custom-trained YOLO model, tracking algorithms, and spatial analysis to generate structured insights.

---

## 📌 Features

- 🔍 **YOLOv5 Object Detection** for:
  - Team A players (white circles)
  - Team B players (black triangles)
  - Ball (circle)
- 🧠 **Consistent Player Tracking** using Hungarian Algorithm.
- 🕒 **Frame Parsing with Timestamps**.
- 📊 **Event Detection Engine**:
  - **Passes**: Based on ball movement within same team.
  - **Tackles**: Based on possession changes.
  - **Goals**: Based on ball location in goalpost region.
- 🧾 **Structured Output**:
  - `output1.json`: Frame-by-frame data.
  - `phase2_event_output1.json`: Event logs with metadata.

---

## 🎯 Project Goals

- Automate tactical match analysis.
- Convert raw video data into actionable insights.

---

## 🛠️ Tech Stack

| Component        | Tech Used            |
|------------------|----------------------|
| Detection        | YOLOv8 (Custom-trained) |
| Tracking         | Hungarian Algorithm   |
| Event Analysis   | Python, NumPy, JSON   |
| Visualization    | Matplotlib, OpenCV    |

---

## 📂 Folder Structure
FOOTYMIND/ 
│ ├── model/
│ ├── images/ 
│ ├── input/ 
│ ├── labels/ 
│ ├── yolov5/ 
│ ├── data.yaml 
│ ├── helper.py 
│ ├── helper1.py 
│ ├── runner.py 
│ ├── output.json  
│ └── output1.json 
│ ├── phases/ 
│ ├── phase1/ 
│ ├── phase2/ 
│ ├── phase2.5/ 
│ ├── phase3/  
│ └── phase4/
│ ├── venv/ 
├── .gitignore 
├── README.md 
├── requirements.txt

