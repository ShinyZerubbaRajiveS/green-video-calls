from app import db
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert the user object to a dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class VideoCall(db.Model):
    __tablename__ = 'video_call'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    meeting_link = Column(String, nullable=False)
    username = Column(String(80), nullable=True)  # Optional field
    email = Column(String(120), nullable=True)     # Optional field
    duration = Column(Integer, nullable=False)
    resolution = Column(String, nullable=False)
    connection_speed = Column(String, nullable=False)
    device_specs = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    carbon_footprint = relationship("CarbonFootprint", uselist=False, back_populates="video_call")

    def to_dict(self):
        """Convert the video call object to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'meeting_link': self.meeting_link,
            'username': self.username,
            'email': self.email,
            'duration': self.duration,
            'resolution': self.resolution,
            'connection_speed': self.connection_speed,
            'device_specs': self.device_specs,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<VideoCall(id={self.id}, user_id={self.user_id}, meeting_link='{self.meeting_link}')>"

class CarbonFootprint(db.Model):
    __tablename__ = 'carbon_footprint'

    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey('video_call.id'), nullable=False)
    energy_consumption = Column(Float, nullable=False)
    carbon_emissions = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    video_call = relationship("VideoCall", back_populates="carbon_footprint")

    def to_dict(self):
        """Convert the carbon footprint object to a dictionary."""
        return {
            'id': self.id,
            'call_id': self.call_id,
            'energy_consumption': self.energy_consumption,
            'carbon_emissions': self.carbon_emissions,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<CarbonFootprint(id={self.id}, call_id={self.call_id}, energy_consumption={self.energy_consumption})>"

class Recommendation(db.Model):
    __tablename__ = 'recommendation'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recommendation_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert the recommendation object to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recommendation_text': self.recommendation_text,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<Recommendation(id={self.id}, user_id={self.user_id}, recommendation_text='{self.recommendation_text}')>"