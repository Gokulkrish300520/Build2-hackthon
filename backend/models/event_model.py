from sqlalchemy import Column, Integer, Float, String
from database.db import Base

class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String)
    event_type = Column(Integer)
    risk_level = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    radius_m = Column(Integer)
    confidence = Column(Integer)
    timestamp = Column(Integer)