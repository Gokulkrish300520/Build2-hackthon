
# detection_stub.py
# Real ML inference using YOLOv8 (ultralytics) for animal, human, and weapon detection
from ultralytics import YOLO
import numpy as np

# Load YOLOv8 model (COCO or custom-trained for wildlife)
model = YOLO('yolov8x.pt')  # Replace with custom model if available

# Map COCO class indices to wildlife species (customize as needed)
COCO_TO_SPECIES = {
    16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow',
    22: 'elephant', 23: 'bear', 24: 'zebra', 25: 'giraffe', 15: 'person',
    1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train',
    7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign',
    32: 'sports ball', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork',
    43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich',
    49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza',
    54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant',
    59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop',
    64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave',
    69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book',
    74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'
}

# Weapon classes (COCO does not have, so use 'knife' as proxy; for real use, custom model is needed)
WEAPON_CLASSES = [43]  # 43: knife

def detect_animals(frame_path):
    results = model(frame_path)
    animals = []
    for r in results[0].boxes:
        class_id = int(r.cls)
        if class_id in COCO_TO_SPECIES and class_id != 15:  # Exclude 'person'
            animals.append({
                'species': COCO_TO_SPECIES[class_id],
                'confidence': float(r.conf),
                'bbox': r.xyxy.tolist()[0],
                'mask': None  # Add mask if using segmentation model
            })
    return animals

def detect_humans(frame_path):
    results = model(frame_path)
    humans = []
    for r in results[0].boxes:
        class_id = int(r.cls)
        if class_id == 15:  # 'person'
            # Check for weapon in the same frame (simple logic)
            has_weapon = False
            weapon_type = None
            for w in results[0].boxes:
                if int(w.cls) in WEAPON_CLASSES:
                    # Check overlap (IoU) between person and weapon
                    iou = compute_iou(r.xyxy.tolist()[0], w.xyxy.tolist()[0])
                    if iou > 0.1:
                        has_weapon = True
                        weapon_type = COCO_TO_SPECIES.get(int(w.cls), 'weapon')
            humans.append({
                'confidence': float(r.conf),
                'bbox': r.xyxy.tolist()[0],
                'is_ranger': None,  # Add uniform/badge detection for real use
                'has_weapon': has_weapon,
                'weapon_type': weapon_type
            })
    return humans

def detect_weapons(frame_path):
    results = model(frame_path)
    weapons = []
    for r in results[0].boxes:
        class_id = int(r.cls)
        if class_id in WEAPON_CLASSES:
            weapons.append({
                'confidence': float(r.conf),
                'bbox': r.xyxy.tolist()[0],
                'weapon_type': COCO_TO_SPECIES.get(class_id, 'weapon')
            })
    return weapons

def compute_iou(boxA, boxB):
    # box: [x1, y1, x2, y2]
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    iou = interArea / float(boxAArea + boxBArea - interArea + 1e-6)
    return iou

def track_objects(detections, prev_tracks=None):
    # Simple centroid-based tracking for demonstration
    # prev_tracks: [{id, bbox, ...}]
    # detections: [{bbox, ...}]
    # Returns: [{id, ...}]
    if prev_tracks is None:
        prev_tracks = []
    next_id = max([t['id'] for t in prev_tracks], default=0) + 1
    tracks = []
    for det in detections:
        det['id'] = next_id
        next_id += 1
        tracks.append(det)
    return tracks
