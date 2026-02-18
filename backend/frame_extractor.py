import cv2
import os
from backend.db import SessionLocal
from backend.models import Frame, Video

def extract_frames(video_id, video_path, fps=1):
    cap = cv2.VideoCapture(video_path)
    db = SessionLocal()
    frame_count = 0
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        if int(frame_count % max(1, int(video_fps // fps))) == 0:
            # Save frame to disk (optional)
            frame_filename = f"backend/frames/{video_id}_{frame_count}.jpg"
            os.makedirs(os.path.dirname(frame_filename), exist_ok=True)
            cv2.imwrite(frame_filename, frame)
            # Store frame metadata
            db_frame = Frame(video_id=video_id, frame_number=frame_count, timestamp=timestamp)
            db.add(db_frame)
            db.commit()
        frame_count += 1
    cap.release()
    db.close()
