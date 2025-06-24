import cv2
import torch
import sys
import os

# Add yolov5 directory to path
YOLOV5_PATH = os.path.join(os.path.dirname(__file__), 'model/yolov5')
sys.path.append(YOLOV5_PATH)

from models.common import DetectMultiBackend
from utils.general import non_max_suppression
from utils.augmentations import letterbox
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLOv5 model
model_path = os.path.join(YOLOV5_PATH, 'runs/train/exp2/weights/best.pt')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = DetectMultiBackend(model_path, device=device)
stride, names = model.stride, model.names
model.eval()

# Init tracker
tracker = DeepSort(max_age=30)

# Load video
video_path = './model/input/lose.mp4'
cap = cv2.VideoCapture(video_path)

# Video writer
output_path = 'output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img = letterbox(frame, new_shape=640, stride=stride)[0]
    img = img.transpose((2, 0, 1))[::-1]
    img = torch.from_numpy(img).to(device).float() / 255.0
    img = img.unsqueeze(0)

    pred = model(img)
    pred = non_max_suppression(pred, 0.25, 0.45)[0]

    detections = []
    for *xyxy, conf, cls in pred:
        bbox = [int(xyxy[0]), int(xyxy[1]), int(xyxy[2] - xyxy[0]), int(xyxy[3] - xyxy[1])]
        detections.append((bbox, conf.item(), int(cls.item())))

    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue
        ltrb = track.to_ltrb()
        cls_id = track.det_class
        track_id = track.track_id
        label = f'{names[cls_id]}_{track_id}'
        cv2.rectangle(frame, (int(ltrb[0]), int(ltrb[1])), (int(ltrb[2]), int(ltrb[3])), (0, 255, 0), 2)
        cv2.putText(frame, label, (int(ltrb[0]), int(ltrb[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    writer.write(frame)
    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
writer.release()
cv2.destroyAllWindows()
