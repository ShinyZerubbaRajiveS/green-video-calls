from app import db  # Adjust the import path based on your project structure
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
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
            'created_at': self.created_at.isoformat()  # Convert to ISO format for JSON serialization
        }

class VideoCall(db.Model):
    __tablename__ = 'video_calls'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    meeting_link = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False, default=0)
    resolution = Column(String(50))
    connection_speed = Column(String(50))
    device_specs = Column(String(255))

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
            'device_specs': self.device_specs
        }

class CarbonFootprint(db.Model):
    __tablename__ = 'carbon_footprints'

    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey('video_calls.id'), nullable=False)
    energy_consumption = Column(Float, nullable=False)  # Energy consumption in kWh
    carbon_emissions = Column(Float, nullable=False)  # CO2 emissions in kg
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert the carbon footprint object to a dictionary."""
        return {
            'id': self.id,
            'call_id': self.call_id,
            'energy_consumption': self.energy_consumption,
            'carbon_emissions': self.carbon_emissions,
            'created_at': self.created_at.isoformat()  # Convert to ISO format for JSON serialization
        }

class Recommendation(db.Model):
    __tablename__ = 'recommendations'

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
            'created_at': self.created_at.isoformat()  # Convert to ISO format for JSON serialization
        }
