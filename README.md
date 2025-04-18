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
- Lay foundation for advanced analytics (e.g., heatmaps, pass networks).

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
FOOTYMIND/ │ ├── model/ # Object detection components │ ├── images/ # Sample images │ ├── input/ # Frame-wise input images │ ├── labels/ # YOLO-style label files │ ├── yolov5/ # YOLOv5 model directory │ ├── data.yaml # Dataset configuration for training │ ├── helper.py # Object parsing and frame utilities │ ├── helper1.py # (Possibly backup/extended helper) │ ├── runner.py # Script to run detection & output │ ├── output.json # Raw positional output (if any) │ └── output1.json # Cleaned positional output │ ├── phases/ │ ├── phase1/ # Tracking logic & player indexing │ └── phase2/ # Event classification logic │ ├── venv/ # Python virtual environment ├── .gitignore ├── README.md ├── requirements.txt

