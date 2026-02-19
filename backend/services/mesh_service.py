from fastapi import WebSocket
from typing import Dict
import json
from database.db import SessionLocal
from models.event_model import Event

connected_nodes: Dict[str, WebSocket] = {}
seen_events = set()

async def register_node(node_id: str, websocket: WebSocket):
    print(f"Registering node: {node_id}")
    connected_nodes[node_id] = websocket
    print("CURRENT CONNECTED:", list(connected_nodes.keys()))

    # If ranger connects, send latest event immediately
    if node_id.startswith("RANGER"):
        db = SessionLocal()

        latest_event = (
            db.query(Event)
            .order_by(Event.timestamp.desc())
            .first()
        )

        db.close()

        if latest_event:
            event_payload = {
                "event_id": latest_event.event_id,
                "event_type": latest_event.event_type,
                "risk_level": latest_event.risk_level,
                "lat": latest_event.lat,
                "lon": latest_event.lon,
                "radius_m": latest_event.radius_m,
                "confidence": latest_event.confidence,
                "timestamp": latest_event.timestamp,
                "ttl": 1,
                "type": "event",
            }

            print("Sending latest event to Ranger")
            await websocket.send_text(json.dumps(event_payload))

def unregister_node(node_id: str):
    if node_id in connected_nodes:
        del connected_nodes[node_id]

async def broadcast_event(sender_id: str, event: dict):
    print("CONNECTED NODES:", list(connected_nodes.keys()))
    print("SENDER:", sender_id)

    for node_id, ws in connected_nodes.items():
        if node_id != sender_id:
            print(f"Broadcasting to {node_id}")
            await ws.send_text(json.dumps(event))