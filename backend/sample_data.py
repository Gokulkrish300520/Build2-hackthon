
from backend.db import SessionLocal
from backend.models import Alert, Patrol, NetworkStatus, IntelligenceReport, Detection, Frame

# Sample Alerts
alerts = [
    Alert(title='Unauthorized Movement Detected', description='Potential poacher activity near water source', severity='critical', status='active', location='Northern Corridor', camera_id=1, timestamp=1700000000),
    Alert(title='Wildlife Aggregation', description='Unusual elephant herd gathering detected', severity='warning', status='acknowledged', location='Eastern Reserve', camera_id=2, timestamp=1700001000),
    Alert(title='Network Connectivity Issue', description='Node connection degradation detected', severity='info', status='resolved', location='Central Area', camera_id=3, timestamp=1700002000),
    Alert(title='Suspicious Vehicle Detected', description='Unregistered vehicle near reserve boundary', severity='critical', status='active', location='Southern Basin', camera_id=4, timestamp=1700003000),
    Alert(title='Camera Offline', description='Camera SB-01 not responding to heartbeat', severity='warning', status='acknowledged', location='Southern Basin', camera_id=5, timestamp=1700004000),
    Alert(title='Fence Line Breach', description='Perimeter sensor triggered near gate 4', severity='warning', status='acknowledged', location='Western Plains', camera_id=6, timestamp=1700005000),
    Alert(title='Patrol Communication Lost', description='Lost contact with Delta team for 3 minutes', severity='info', status='resolved', location='Central Area', camera_id=7, timestamp=1700006000),
    Alert(title='Scheduled Maintenance Reminder', description='Camera NC-02 due for quarterly service', severity='info', status='resolved', location='Northern Corridor', camera_id=8, timestamp=1700007000),
]

# Sample Patrols
patrols = [
    Patrol(team_name='Alpha', route='North-East', status='active', start_time=1700000000, end_time=1700003600),
    Patrol(team_name='Bravo', route='Central', status='completed', start_time=1699996400, end_time=1699999000),
    Patrol(team_name='Charlie', route='South-West', status='active', start_time=1700002000, end_time=1700005600),
    Patrol(team_name='Delta', route='West', status='lost', start_time=1700003000, end_time=1700006600),
]

# Sample Network Status
network_statuses = [
    NetworkStatus(camera_id=1, patrol_id=1, status='online', last_checked=1700000000, issues=''),
    NetworkStatus(camera_id=2, patrol_id=2, status='degraded', last_checked=1700001000, issues='Packet loss'),
    NetworkStatus(camera_id=3, patrol_id=3, status='offline', last_checked=1700002000, issues='No signal'),
    NetworkStatus(camera_id=4, patrol_id=4, status='online', last_checked=1700003000, issues=''),
]

# Sample Intelligence Reports
intelligence_reports = [
    IntelligenceReport(generated_at=1700000000, summary='Poaching risk high in Northern Corridor', recommendations='Increase patrols, deploy drones', trend_data='{"zone":"NC","risk":0.8}'),
    IntelligenceReport(generated_at=1700001000, summary='Elephant aggregation detected', recommendations='Monitor herd, alert rangers', trend_data='{"zone":"ER","risk":0.5}'),
]

# Sample Detections for Overview/Heatmap
frames = [
    Frame(video_id='VID-01', frame_number=100, timestamp=1700000000),
    Frame(video_id='VID-02', frame_number=200, timestamp=1700001000)
]

def main():
    db = SessionLocal()
    db.add_all(alerts)
    db.add_all(patrols)
    db.add_all(network_statuses)
    db.add_all(intelligence_reports)
    db.commit()
    # Now add frames and detections, linking frame_id after commit
    for frame in frames:
        db.add(frame)
    db.commit()
    frame_objs = db.query(Frame).all()
    detections = [
        Detection(frame_id=frame_objs[0].id, type='human', bbox='{"x":100,"y":200,"w":50,"h":80}', confidence=0.95, risk_score=0.9, is_poacher=True),
        Detection(frame_id=frame_objs[1].id, type='animal', bbox='{"x":120,"y":220,"w":60,"h":90}', confidence=0.88, species='Elephant', risk_score=0.2, is_poacher=False),
    ]
    db.add_all(detections)
    db.commit()
    db.close()

    print('Sample data injected successfully!')

if __name__ == '__main__':
    main()
