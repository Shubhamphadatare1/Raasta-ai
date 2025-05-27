import sys
import os
import torch
import cv2
import numpy as np
import pathlib

# 🔧 Patch PosixPath for Windows compatibility
original_posix_path = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Add yolov5 to path
sys.path.append(os.path.join(os.getcwd(), 'yolov5'))

# 📦 YOLOv5 utilities
from models.common import DetectMultiBackend
from utils.augmentations import letterbox
from utils.general import non_max_suppression

# Load YOLOv5 model
model = DetectMultiBackend('models/helmet_yolov5s.pt', device='cpu')

# ✅ Restore PosixPath
pathlib.PosixPath = original_posix_path

def detect_helmets(image_path):
    img0 = cv2.imread(image_path)
    if img0 is None:
        print("❌ Error: Image not found at", image_path)
        return

    # 🧪 Preprocess: resize & format for YOLOv5
    img = letterbox(img0, 640, stride=32, auto=True)[0]
    img = img.transpose((2, 0, 1))  # HWC to CHW
    img = np.ascontiguousarray(img)

    img = torch.from_numpy(img).to('cpu')
    img = img.float() / 255.0  # 0 - 255 → 0.0 - 1.0
    img = img.unsqueeze(0)     # Add batch dimension

    # 🚀 Inference
    pred = model(img)
    pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45)[0]

    # 🖼️ Draw results
    annotated = img0.copy()
    for *xyxy, conf, cls in pred:
        label = model.names[int(cls)]
        color = (0, 255, 0) if label.lower() == "helmet" else (0, 0, 255)
        cv2.rectangle(annotated, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, 2)
        cv2.putText(annotated, f'{label} {conf:.2f}', (int(xyxy[0]), int(xyxy[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # 🔍 Show output
    cv2.imshow("Helmet Detection", annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 🚦 Run script
if __name__ == "__main__":
    detect_helmets("data/test_image.jpg")