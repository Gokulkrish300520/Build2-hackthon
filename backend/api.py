from fastapi import APIRouter, HTTPException
from backend.db import SessionLocal
from backend.models import (
    IntelligenceReport, NetworkStatus, Patrol, PatrolReport, Camera, Video, Detection, Alert, PoachingEvent, Species, Frame
)

router = APIRouter()

@router.get('/intelligence/trends')
def get_intelligence_trends():
    db = SessionLocal()
    reports = db.query(IntelligenceReport).all()
    db.close()
    return {'trends': [
        {
            'id': r.id,
            'generated_at': r.generated_at,
            'trend_data': r.trend_data
        } for r in reports
    ]}

@router.get('/intelligence/recommendations')
def get_intelligence_recommendations():
    db = SessionLocal()
    reports = db.query(IntelligenceReport).all()
    db.close()
    return {'recommendations': [
        {
            'id': r.id,
            'generated_at': r.generated_at,
            'recommendations': r.recommendations
        } for r in reports
    ]}

@router.post('/intelligence/report')
def generate_intelligence_report(summary: str, recommendations: str, trend_data: str):
    db = SessionLocal()
    report = IntelligenceReport(generated_at=0, summary=summary, recommendations=recommendations, trend_data=trend_data)
    db.add(report)
    db.commit()
    db.close()
    return {'success': True}
@router.get('/network/')
def get_network_status():
    db = SessionLocal()
    statuses = db.query(NetworkStatus).all()
    db.close()
    return {'network_status': [
        {
            'id': s.id,
            'camera_id': s.camera_id,
            'patrol_id': s.patrol_id,
            'status': s.status,
            'last_checked': s.last_checked,
            'issues': s.issues
        } for s in statuses
    ]}
@router.get('/patrols/')
def get_patrols():
    db = SessionLocal()
    patrols = db.query(Patrol).all()
    db.close()
    return {'patrols': [
        {
            'id': p.id,
            'team_name': p.team_name,
            'route': p.route,
            'status': p.status,
            'start_time': p.start_time,
            'end_time': p.end_time
        } for p in patrols
    ]}

@router.post('/patrols/report')
def submit_patrol_report(patrol_id: int, description: str, sightings: str):
    db = SessionLocal()
    report = PatrolReport(patrol_id=patrol_id, timestamp=0, description=description, sightings=sightings)
    db.add(report)
    db.commit()
    db.close()
    return {'success': True}
@router.get('/cameras/')
def get_cameras():
    db = SessionLocal()
    cameras = db.query(Camera).all()
    db.close()
    return {'cameras': [
        {
            'id': c.id,
            'name': c.name,
            'location': c.location,
            'status': c.status
        } for c in cameras
    ]}

@router.get('/cameras/{camera_id}/feeds')
def get_camera_feeds(camera_id: int):
    db = SessionLocal()
    videos = db.query(Video).filter(Video.camera_id == camera_id).all()
    db.close()
    return {'feeds': [
        {
            'id': v.id,
            'filename': v.filename,
            'upload_time': v.upload_time,
            'status': v.status
        } for v in videos
    ]}

@router.get('/cameras/{camera_id}/detections')
def get_camera_detections(camera_id: int):
    db = SessionLocal()
    videos = db.query(Video).filter(Video.camera_id == camera_id).all()
    detections = []
    for v in videos:
        for frame in v.frames:
            for det in frame.detections:
                detections.append({
                    'frame_number': frame.frame_number,
                    'timestamp': frame.timestamp,
                    'type': det.type,
                    'bbox': det.bbox,
                    'species': det.species,
                    'confidence': det.confidence,
                    'is_poacher': det.is_poacher,
                    'risk_score': det.risk_score
                })
    db.close()
    return {'detections': detections}
@router.get('/alerts/')
def get_alerts(severity: str = None, status: str = None, search: str = None):
    db = SessionLocal()
    query = db.query(Alert)
    if severity:
        query = query.filter(Alert.severity == severity)
    if status:
        query = query.filter(Alert.status == status)
    if search:
        query = query.filter(Alert.title.ilike(f'%{search}%'))
    alerts = query.all()
    db.close()
    return {'alerts': [
        {
            'id': a.id,
            'title': a.title,
            'location': a.location,
            'camera_id': a.camera_id,
            'severity': a.severity,
            'status': a.status,
            'timestamp': a.timestamp,
            'description': a.description
        } for a in alerts
    ]}

@router.post('/alerts/acknowledge')
def acknowledge_alert(alert_id: int):
    db = SessionLocal()
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.status = 'acknowledged'
        db.commit()
    db.close()
    return {'success': True}

@router.post('/alerts/resolve')
def resolve_alert(alert_id: int):
    db = SessionLocal()
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.status = 'resolved'
        db.commit()
    db.close()
    return {'success': True}

@router.post('/alerts/export')
def export_alerts():
    db = SessionLocal()
    alerts = db.query(Alert).all()
    db.close()
    # Export logic (CSV/Excel) can be added here
    return {'success': True, 'message': 'Exported'}

@router.get("/videos/{video_id}/detections/")
def get_detections(video_id: str):
    db = SessionLocal()
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        db.close()
        raise HTTPException(status_code=404, detail="Video not found")
    detections = []
    for frame in video.frames:
        for det in frame.detections:
            detections.append({
                "frame_number": frame.frame_number,
                "timestamp": frame.timestamp,
                "type": det.type,
                "bbox": det.bbox,
                "species": det.species,
                "confidence": det.confidence,
                "is_poacher": det.is_poacher,
                "risk_score": det.risk_score
            })
    db.close()
    return {"detections": detections}

@router.get("/poaching_events/")
def get_poaching_events():
    db = SessionLocal()
    events = db.query(PoachingEvent).all()
    result = []
    for event in events:
        result.append({
            "id": event.id,
            "human_id": event.human_id,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "location": event.location,
            "species_affected": event.species_affected,
            "description": event.description
        })
    db.close()
    return {"poaching_events": result}

@router.get("/alerts/high_risk/")
def get_high_risk_alerts():
    db = SessionLocal()
    # Return all human detections with risk_score >= 0.7
    alerts = db.query(Detection).filter(Detection.type == "human", Detection.risk_score >= 0.7).all()
    result = []
    for det in alerts:
        result.append({
            "frame_id": det.frame_id,
            "bbox": det.bbox,
            "risk_score": det.risk_score,
            "is_poacher": det.is_poacher
        })
    db.close()
    return {"high_risk_alerts": result}

@router.get("/stats/species/")
def get_species_stats():
    db = SessionLocal()
    # Count animal detections by species
    from sqlalchemy import func
    species_counts = db.query(Detection.species, func.count(Detection.id)).filter(Detection.type == "animal").group_by(Detection.species).all()
    stats = [{"species": s, "count": c} for s, c in species_counts]
    db.close()
    return {"species_stats": stats}

@router.get("/stats/poaching_trends/")
def get_poaching_trends():
    db = SessionLocal()
    # Count high-risk detections by hour (demo)
    from sqlalchemy import func
    from backend.models import Frame
    results = db.query(Frame.timestamp, Detection.risk_score).join(Detection, Detection.frame_id == Frame.id).filter(Detection.type == "human", Detection.risk_score >= 0.7).all()
    # Group by hour
    from collections import Counter
    hours = [int(ts // 3600) for ts, _ in results]
    trends = Counter(hours)
    db.close()
    return {"poaching_trends": dict(trends)}
