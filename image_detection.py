import sys
import os
import cv2
import torch

# Add relative path to yolov5
YOLOV5_PATH = os.path.join('model', 'yolov5')
sys.path.append(YOLOV5_PATH)

from models.common import DetectMultiBackend
from utils.general import non_max_suppression
from utils.augmentations import letterbox

# Load YOLOv5 model (relative path to weights)
model_path = os.path.join(YOLOV5_PATH, 'runs', 'train', 'exp2', 'weights', 'best.pt')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = DetectMultiBackend(model_path, device=device)
stride, names = model.stride, model.names
model.eval()

# Load input image (relative path)
image_path = os.path.join('model', 'images', 'train', 'img00.jpg')
img0 = cv2.imread(image_path)
assert img0 is not None, f"Image not found at {image_path}"

# Resize and pad image
img = letterbox(img0, new_shape=640, stride=stride, auto=False)[0]

# Compute scaling ratio and padding
h0, w0 = img0.shape[:2]
r = min(640 / w0, 640 / h0)
new_unpad = (int(round(w0 * r)), int(round(h0 * r)))
pad_w, pad_h = 640 - new_unpad[0], 640 - new_unpad[1]
pad_w /= 2
pad_h /= 2

# Preprocessing
img = img.transpose((2, 0, 1))[::-1].copy()
img = torch.from_numpy(img).to(device).float() / 255.0
img = img.unsqueeze(0)

# Inference
pred = model(img)
pred = non_max_suppression(pred, 0.25, 0.45)[0]

# Draw bounding boxes
for *xyxy, conf, cls in pred:
    x1, y1, x2, y2 = xyxy
    x1 = (x1 - pad_w) / r
    y1 = (y1 - pad_h) / r
    x2 = (x2 - pad_w) / r
    y2 = (y2 - pad_h) / r
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

    label = f'{names[int(cls.item())]} {conf:.2f}'
    cv2.rectangle(img0, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(img0, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Show and save result
output_path = os.path.join('output_image.jpg')
cv2.imshow('Image Detection', img0)
cv2.imwrite(output_path, img0)
cv2.waitKey(0)
cv2.destroyAllWindows()
