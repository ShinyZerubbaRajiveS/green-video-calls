import platform
import speedtest
import requests
import time
import subprocess
import logging
from app.models import Recommendation, db

def calculate_carbon_footprint(duration, resolution, connection_speed, device_specs):
    """Calculate carbon footprint based on call parameters."""
    # Energy consumption factors (kWh per minute)
    factors = {
        'resolution': {
            '480p': 0.0015,
            '720p': 0.003,
            '1080p': 0.006,
            '4K': 0.012
        },
        'connection': {
            'slow': 0.001,
            'average': 0.002,
            'fast': 0.004
        },
        'device': {
            'low': 0.001,
            'medium': 0.002,
            'high': 0.004
        }
    }

    # Calculate total energy (kWh)
    energy = (
        factors['resolution'].get(resolution, 0.003) +
        factors['connection'].get(connection_speed, 0.002) +
        factors['device'].get(device_specs.get('type', 'medium'), 0.002)
    ) * duration

    # Carbon emissions (kg CO2) - using average US grid factor
    carbon = energy * 0.4

    return {
        'energy_consumption': round(energy, 4),
        'carbon_emissions': round(carbon, 4)
    }

def generate_recommendations(user_id, footprint):
    """Generate energy-saving recommendations."""
    recommendations = []
    
    if footprint.carbon_emissions > 0.1:  # 100g CO2
        recommendations.append(
            "Consider reducing video quality to save energy"
        )
    
    if footprint.energy_consumption > 0.5:  # 0.5 kWh
        recommendations.append(
            "Try shorter meetings or audio-only for long sessions"
        )
    
    # Save to database
    db_recommendations = [
        Recommendation(
            user_id=user_id,
            recommendation_text=text
        ) for text in recommendations
    ]
    
    db.session.add_all(db_recommendations)
    db.session.commit()
    
    return db_recommendations

def get_internet_speed():
    """Measure internet speed using speedtest.net."""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        return {
            'download': round(st.download() / 1_000_000, 2),  # Mbps
            'upload': round(st.upload() / 1_000_000, 2)      # Mbps
        }
    except Exception as e:
        logging.warning(f"Speedtest failed: {e}")
        return {'download': 10, 'upload': 5}  # Default values