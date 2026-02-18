from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Video(Base):
    __tablename__ = 'videos'
    id = Column(String, primary_key=True)
    filename = Column(String)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)
    duration = Column(Float)
    status = Column(String)
    camera_id = Column(Integer, ForeignKey('cameras.id'), nullable=True)
    frames = relationship("Frame", back_populates="video")
    camera = relationship("Camera", back_populates="videos")

class Frame(Base):
    __tablename__ = 'frames'
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String, ForeignKey('videos.id'))
    frame_number = Column(Integer)
    timestamp = Column(Float)
    video = relationship("Video", back_populates="frames")
    detections = relationship("Detection", back_populates="frame")

class Detection(Base):
    __tablename__ = 'detections'
    id = Column(Integer, primary_key=True, autoincrement=True)
    frame_id = Column(Integer, ForeignKey('frames.id'))
    type = Column(String)  # animal/human/weapon
    bbox = Column(JSON)
    mask = Column(JSON, nullable=True)
    confidence = Column(Float)
    species = Column(String, nullable=True)
    human_id = Column(Integer, ForeignKey('humans.id'), nullable=True)
    weapon_type = Column(String, nullable=True)
    is_poacher = Column(Boolean, nullable=True)
    risk_score = Column(Float, nullable=True)
    frame = relationship("Frame", back_populates="detections")

class Human(Base):
    __tablename__ = 'humans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    track_id = Column(String)
    first_seen_frame_id = Column(Integer, ForeignKey('frames.id'))
    last_seen_frame_id = Column(Integer, ForeignKey('frames.id'))
    is_ranger = Column(Boolean, nullable=True)
    is_poacher = Column(Boolean, nullable=True)
    risk_score = Column(Float)


class PoachingEvent(Base):
    __tablename__ = 'poaching_events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    human_id = Column(Integer, ForeignKey('humans.id'))
    start_time = Column(Float)
    end_time = Column(Float)
    location = Column(String, nullable=True)
    species_affected = Column(String, nullable=True)
    description = Column(String)

# Admin UI models
class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    location = Column(String)
    camera_id = Column(Integer, ForeignKey('cameras.id'), nullable=True)
    severity = Column(String)
    status = Column(String)
    timestamp = Column(Float)
    description = Column(String)
    detection_id = Column(Integer, ForeignKey('detections.id'), nullable=True)

class Camera(Base):
    __tablename__ = 'cameras'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    location = Column(String)
    status = Column(String)
    videos = relationship("Video", back_populates="camera")

class Patrol(Base):
    __tablename__ = 'patrols'
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String)
    route = Column(String)
    status = Column(String)
    start_time = Column(Float)
    end_time = Column(Float)

class PatrolReport(Base):
    __tablename__ = 'patrol_reports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    patrol_id = Column(Integer, ForeignKey('patrols.id'))
    timestamp = Column(Float)
    description = Column(String)
    sightings = Column(String)

class NetworkStatus(Base):
    __tablename__ = 'network_status'
    id = Column(Integer, primary_key=True, autoincrement=True)
    camera_id = Column(Integer, ForeignKey('cameras.id'), nullable=True)
    patrol_id = Column(Integer, ForeignKey('patrols.id'), nullable=True)
    status = Column(String)
    last_checked = Column(Float)
    issues = Column(String)

class IntelligenceReport(Base):
    __tablename__ = 'intelligence_reports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    generated_at = Column(Float)
    summary = Column(String)
    recommendations = Column(String)
    trend_data = Column(String)

class Species(Base):
    __tablename__ = 'species'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
