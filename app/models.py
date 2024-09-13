from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'  # Use 'users' to avoid reserved keyword issues

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert the user object to a dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()  # Convert to ISO format for JSON serialization
        }

class VideoCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    resolution = db.Column(db.String(50), nullable=False)
    connection_speed = db.Column(db.Integer, nullable=False)  # Speed in Mbps
    device_specs = db.Column(db.JSON, nullable=False)  # Store device specifications as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert the video call object to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'duration': self.duration,
            'resolution': self.resolution,
            'connection_speed': self.connection_speed,
            'device_specs': self.device_specs,
            'created_at': self.created_at.isoformat()  # Convert to ISO format for JSON serialization
        }

class CarbonFootprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey('video_call.id'), nullable=False)
    energy_consumption = db.Column(db.Float, nullable=False)  # Energy consumption in kWh
    carbon_emissions = db.Column(db.Float, nullable=False)  # CO2 emissions in kg
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recommendation_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert the recommendation object to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recommendation_text': self.recommendation_text,
            'created_at': self.created_at.isoformat()  # Convert to ISO format for JSON serialization
        }