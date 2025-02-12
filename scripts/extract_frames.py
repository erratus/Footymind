import cv2
import os

video_path = "../data/soccer_videos/match.mp4"
output_folder = "../data/frames"

os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_rate = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(frame_rate)

count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if count % frame_interval == 0:
        cv2.imwrite(f"{output_folder}/frame_{count}.jpg", frame)
    count += 1
cap.release()
