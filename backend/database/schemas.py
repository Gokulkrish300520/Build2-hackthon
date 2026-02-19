from pydantic import BaseModel
from typing import Optional
import time


# =========================
# Event Schemas
# =========================

class EventBase(BaseModel):
    event_id: int
    node_id: Optional[str] = None
    event_type: int
    risk_level: int
    lat: float
    lon: float
    radius_m: int
    confidence: int
    timestamp: int = int(time.time())
    ttl: Optional[int] = 4


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    class Config:
        from_attributes = True


# =========================
# Node Schemas
# =========================

class NodeBase(BaseModel):
    node_id: str
    battery: int
    status: Optional[str] = "ONLINE"


class NodeResponse(NodeBase):
    last_seen: int

    class Config:
        from_attributes = True


# =========================
# Heartbeat Schema
# =========================

class Heartbeat(BaseModel):
    type: str = "heartbeat"
    node_id: str
    battery: int