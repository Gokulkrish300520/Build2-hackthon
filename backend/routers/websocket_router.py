from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from services.mesh_service import register_node, unregister_node, broadcast_event
from services.heartbeat_service import update_heartbeat
from database.db import SessionLocal
from models.event_model import Event
from database.schemas import EventCreate, Heartbeat
from pydantic import ValidationError
from services.routing_service import should_process_event, decrement_ttl
from services.risk_engine import process_event
from services.mesh_service import broadcast_event

router = APIRouter()

@router.websocket("/ws/{node_id}")
async def websocket_endpoint(websocket: WebSocket, node_id: str):
    await websocket.accept()
    await register_node(node_id, websocket)

    try:
        while True:
            # ✅ Define data here
            data = await websocket.receive_text()

            message = json.loads(data)

            msg_type = message.get("type")

            if msg_type == "heartbeat":
                heartbeat = Heartbeat(**message)
                update_heartbeat(heartbeat.node_id, heartbeat.battery)

            elif msg_type == "event":
                event_data = EventCreate(**message)
                await handle_event(node_id, event_data.dict())

    except WebSocketDisconnect:
        unregister_node(node_id)

    except Exception as e:
        print("WebSocket error:", e)
        unregister_node(node_id)



async def handle_event(sender_id: str, message: dict):

    event_id = message["event_id"]

    # Deduplication
    if not should_process_event(event_id):
        return

    # Recalculate risk + radius
    message = process_event(message)

    # TTL handling
    updated_event = decrement_ttl(message)
    if not updated_event:
        return

    # Store in DB
    db = SessionLocal()

    event = Event(
        event_id=updated_event["event_id"],
        node_id=sender_id,
        event_type=updated_event["event_type"],
        risk_level=updated_event["risk_level"],
        lat=updated_event["lat"],
        lon=updated_event["lon"],
        radius_m=updated_event["radius_m"],
        confidence=updated_event["confidence"],
        timestamp=updated_event["timestamp"]
    )

    db.merge(event)
    db.commit()
    db.close()

    # Forward to other nodes
    await broadcast_event(sender_id, updated_event)