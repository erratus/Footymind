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
| Detection        | YOLOv5 (Custom-trained) |
| Tracking         | Strong sort, Hungarian Algorithm   |
| Event Analysis   | Python, NumPy, JSON   |
| Visualization    | Matplotlib, OpenCV    |

---

## 📂 Folder Structure
FOOTYMIND/  <br>
│ ├── data #contains data <br>
│ ├── exp2/ #contains the modal <br>  
│ ├── phases/ <br>
│ │ ├── phase1/ <br>
│ │ ├── phase2/ <br>
│ │ ├── phase2.5/ <br>
│ │ ├── phase3/  <br>
│ │ └── phase4/<br>
│ ├── venv/ <br>
├── .gitignore <br>
├── README.md <br>
├── requirements.txt<br>


---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/erratus/FootyMind.git
cd FootyMind
```

### 2. Install Dependencies

```bash
pip install numpy scipy opencv-python
```
### 3. Prepare YOLO Labels

Place all YOLO .txt labels (per frame) inside phases/phase1/yolo_labels_raw/.
Each line in a .txt should follow:

```bash
<class_id> <center_x> <center_y> <width> <height>
```

### 4. Train the yolov5 model 
### 5. Run the Pipeline
```bash
# Step 1: Convert YOLO detections to frame-wise position JSON
python phases/phase1/track_and_export.py

# Step 2: Generate event logs from the positions
python phases/phase2/events_classifier.py

```

🔮 Future Improvements
Add offside, foul, and interception detection.

Build interactive dashboard (e.g., with Streamlit).

Integrate predictive models (xG, pass success rate).

📜 License
This project is licensed under the MIT License.

🙌 Acknowledgements
Ultralytics YOLOv8

OpenCV & NumPy

Hungarian Algorithm (via SciPy)

