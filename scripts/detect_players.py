import torch

model = torch.hub.load("ultralytics/yolov5", "yolov5s")

def detect_players(image_path):
    results = model(image_path)
    return results.pandas().xyxy[0]

player_positions = detect_players("../data/frames/frame_0.jpg")
print(player_positions)
