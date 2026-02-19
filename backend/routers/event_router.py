from fastapi import APIRouter
from database.db import SessionLocal
from models.event_model import Event
from database.schemas import EventResponse
from typing import List

router = APIRouter()

@router.get("/events", response_model=List[EventResponse])
def get_events():
    db = SessionLocal()
    events = db.query(Event).all()
    db.close()
    return events