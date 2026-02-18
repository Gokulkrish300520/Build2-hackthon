# Wildlife Anti-Poaching Backend

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the backend:
   ```bash
   uvicorn backend.app:app --reload
   ```

## API Endpoints

- `POST /upload_video/` — Upload a video file
- `GET /videos/{video_id}/detections/` — Get detections for a video
- `GET /poaching_events/` — Query historical poaching events
- `GET /alerts/high_risk/` — Get high-risk poaching alerts
- `GET /stats/species/` — Get species count statistics
- `GET /stats/poaching_trends/` — Get poaching time/trend analytics

## Project Structure

- `backend/app.py` — FastAPI app entry
- `backend/api.py` — API endpoints
- `backend/models.py` — SQLAlchemy models
- `backend/db.py` — Database setup
- `backend/frame_extractor.py` — Frame extraction logic
- `backend/detection_stub.py` — Real ML detection (YOLOv8, Ultralytics)
- `backend/behavior_analysis.py` — Behavior analysis logic

## ML/AI Details

- Uses YOLOv8 (Ultralytics) for animal, human, and weapon detection
- Simple tracking and risk scoring logic included
- Easily extendable for custom models and advanced analytics

## Example Usage

### Upload a video

```bash
curl -F "file=@/path/to/video.mp4" http://localhost:8000/upload_video/
```

### Get detections for a video

```bash
curl http://localhost:8000/videos/<video_id>/detections/
```

### Get high-risk alerts

```bash
curl http://localhost:8000/alerts/high_risk/
```

### Get species statistics

```bash
curl http://localhost:8000/stats/species/
```

### Get poaching trends

```bash
curl http://localhost:8000/stats/poaching_trends/
```

## Notes

- For production, use PostgreSQL and custom-trained models for best results.
- Extend API and models as needed for full analytics and alerting.
