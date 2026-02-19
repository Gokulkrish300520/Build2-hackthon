import time
from database.db import SessionLocal
from models.node_model import Node

OFFLINE_THRESHOLD = 90  # seconds

def update_heartbeat(node_id: str, battery: int):
    db = SessionLocal()
    node = db.query(Node).filter(Node.node_id == node_id).first()

    now = int(time.time())

    if node:
        node.last_seen = now
        node.battery = battery
        node.status = "ONLINE"
    else:
        node = Node(
            node_id=node_id,
            last_seen=now,
            battery=battery,
            status="ONLINE"
        )
        db.add(node)

    db.commit()
    db.close()

def check_offline_nodes():
    db = SessionLocal()
    now = int(time.time())

    nodes = db.query(Node).all()

    for node in nodes:
        if now - node.last_seen > OFFLINE_THRESHOLD:
            node.status = "OFFLINE"

    db.commit()
    db.close()