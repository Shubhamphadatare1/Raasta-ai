import streamlit as st
import sys
import os
import torch
import cv2
import numpy as np
import pathlib
from PIL import Image
import tempfile

# 📌 Setup Paths
original_posix_path = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath  # for Windows compatibility
sys.path.append(os.path.join(os.getcwd(), 'yolov5'))  # ensure YOLOv5 is in path

# 🧠 Import YOLOv5 modules
from models.common import DetectMultiBackend
from utils.augmentations import letterbox
from utils.general import non_max_suppression

# 🔍 Load the YOLOv5 model
model = DetectMultiBackend('models/helmet_yolov5s.pt', device='cpu')
pathlib.PosixPath = original_posix_path  # restore original

st.set_page_config(page_title="🪖 Helmet Detection", layout="centered")
st.title("🪖 Helmet Detection - Upload an Image")
st.write("Upload an image and detect helmets in real-time.")

# 📁 File upload
uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"])

def detect_helmets(img_path):
    img0 = cv2.imread(img_path)
    if img0 is None:
        st.error("❌ Error: Image could not be read.")
        return None

    img = letterbox(img0, 640, stride=32, auto=True)[0]
    img = img.transpose((2, 0, 1))  # HWC to CHW
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to('cpu')
    img = img.float() / 255.0
    img = img.unsqueeze(0)

    pred = model(img)
    pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45)[0]

    # Draw boxes
    for *xyxy, conf, cls in pred:
        label = model.names[int(cls)]
        color = (0, 255, 0) if label.lower() == "helmet" else (0, 0, 255)
        cv2.rectangle(img0, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, 2)
        cv2.putText(img0, f'{label} {conf:.2f}', (int(xyxy[0]), int(xyxy[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return img0

if uploaded_file is not None:
    st.image(uploaded_file, caption="📷 Original Image", use_column_width=True)
    if st.button("🚀 Start Detection"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(uploaded_file.read())
            result_image = detect_helmets(temp.name)

            if result_image is not None:
                st.image(result_image, caption="✅ Detection Result", channels="BGR", use_column_width=True)