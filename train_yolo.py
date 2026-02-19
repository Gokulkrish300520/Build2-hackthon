
from ultralytics import YOLO
import os

# Ensure we're in the right directory or use absolute paths
data_path = "Dataset/Combined/data.yaml"

# Load a model
model = YOLO("yolov8n.pt")  # load a pretrained model

# Train the model
print(f"Starting training with data: {data_path}")
results = model.train(data=data_path, epochs=10, imgsz=640)
print("Training complete.")
