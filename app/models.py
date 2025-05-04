from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    calls = db.relationship('VideoCall', backref='user', lazy=True)

class VideoCall(db.Model):
    __tablename__ = 'video_calls'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    meeting_link = Column(String, nullable=False)
    duration = Column(Integer, default=0)
    resolution = Column(String, default='720p')
    connection_speed = Column(String)
    device_specs = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    carbon_footprint = db.relationship('CarbonFootprint', uselist=False, backref='video_call')

class CarbonFootprint(db.Model):
    __tablename__ = 'carbon_footprints'
    
    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey('video_calls.id'), nullable=False)
    energy_consumption = Column(Float)
    carbon_emissions = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recommendation_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)