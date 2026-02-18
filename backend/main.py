from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
import shutil
import os
from uuid import uuid4
from db import SessionLocal
from models import Video, Frame, Detection
from frame_extractor import extract_frames
from detection_stub import detect_animals, detect_humans, detect_weapons

app = FastAPI()

UPLOAD_DIR = "backend/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload_video/")
async def upload_video(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    video_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{video_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Store video metadata
    db = SessionLocal()
    video = Video(id=video_id, filename=file.filename, status="processing")
    db.add(video)
    db.commit()
    db.close()
    # Trigger async processing
    if background_tasks:
        background_tasks.add_task(process_video_pipeline, video_id, file_path)
    return JSONResponse({"status": "processing", "video_id": video_id})

def process_video_pipeline(video_id, file_path):
    from backend.detection_stub import track_objects
    from backend.behavior_analysis import analyze_behavior
    extract_frames(video_id, file_path, fps=1)
    db = SessionLocal()
    video = db.query(Video).filter(Video.id == video_id).first()
    frames = db.query(Frame).filter(Frame.video_id == video_id).all()
    all_human_tracks = []
    all_animal_tracks = []
    frame_times = []
    prev_human_tracks = []
    prev_animal_tracks = []
    for frame in frames:
        frame_path = f"backend/frames/{video_id}_{frame.frame_number}.jpg"
        animal_dets = detect_animals(frame_path)
        human_dets = detect_humans(frame_path)
        weapon_dets = detect_weapons(frame_path)
        # Tracking (simple demo)
        animal_tracks = track_objects(animal_dets, prev_animal_tracks)
        human_tracks = track_objects(human_dets, prev_human_tracks)
        prev_animal_tracks = animal_tracks
        prev_human_tracks = human_tracks
        all_animal_tracks.append(animal_tracks)
        all_human_tracks.append(human_tracks)
        frame_times.append(frame.timestamp)
        # Store animal detections
        for det in animal_tracks:
            db_det = Detection(
                frame_id=frame.id,
                type="animal",
                bbox=det['bbox'],
                mask=det.get('mask'),
                confidence=det['confidence'],
                species=det['species']
            )
            db.add(db_det)
        # Store human detections
        for det in human_tracks:
            db_det = Detection(
                frame_id=frame.id,
                type="human",
                bbox=det['bbox'],
                confidence=det['confidence'],
                is_poacher=det.get('has_weapon', False),
                weapon_type=det.get('weapon_type'),
                risk_score=0.0  # Will update after behavior analysis
            )
            db.add(db_det)
        # Store weapon detections
        for det in weapon_dets:
            db_det = Detection(
                frame_id=frame.id,
                type="weapon",
                bbox=det['bbox'],
                confidence=det['confidence'],
                weapon_type=det['weapon_type']
            )
            db.add(db_det)
        db.commit()
    # Behavioral analysis (simple demo)
    risk_scores = analyze_behavior(all_human_tracks, all_animal_tracks, frame_times)
    # Update risk scores in DB (demo: assign to all human detections)
    for frame in frames:
        for det in db.query(Detection).filter(Detection.frame_id == frame.id, Detection.type == "human").all():
            det.risk_score = 0.8 if det.is_poacher else 0.1  # Example: high if weapon, else low
    db.commit()
    # Mark video as processed
    video.status = "processed"
    db.commit()
    db.close()
