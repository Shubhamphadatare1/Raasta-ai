import sys
import os
import torch
import cv2
import numpy as np
import pathlib

# 🔧 Patch PosixPath for Windows compatibility
original_posix_path = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# 🧠 Add yolov5 to path
sys.path.append(os.path.join(os.getcwd(), 'yolov5'))

from models.common import DetectMultiBackend
from utils.augmentations import letterbox
from utils.general import non_max_suppression

# ✅ Load YOLOv5 model
model = DetectMultiBackend('models/best.pt', device='cpu')
pathlib.PosixPath = original_posix_path  # restore original

print("Model class names:", model.names)

# 📷 Initialize webcam (0 = default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot access webcam.")
    exit()

print("✅ Webcam started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame.")
        break

    img = letterbox(frame, 640, stride=32, auto=True)[0]
    img = img.transpose((2, 0, 1))  # HWC to CHW
    img = np.ascontiguousarray(img)

    img = torch.from_numpy(img).to('cpu')
    img = img.float() / 255.0
    img = img.unsqueeze(0)

    # 🚀 Inference
    pred = model(img)
    pred = non_max_suppression(pred, conf_thres=0.1, iou_thres=0.45)[0]

    # 📦 Draw detections
    for *xyxy, conf, cls in pred:
        label = model.names[int(cls)]
        color = (0, 255, 0) if label.lower() == "helmet" else (0, 0, 255)
        cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, 2)
        cv2.putText(frame, f'{label} {conf:.2f}', (int(xyxy[0]), int(xyxy[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("🚦 Helmet Detection - Live", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()