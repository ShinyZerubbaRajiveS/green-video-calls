import platform
import speedtest
import cv2
import json
import logging
import requests
import time
import subprocess
from app.models import Recommendation, db

def calculate_carbon_footprint(duration, resolution, connection_speed, device_specs):
    """
    Calculate the carbon footprint based on call duration, video resolution, 
    connection speed, and device specifications.
    """
    # Energy consumption rates (in kWh) for different resolutions
    resolution_energy = {
        '480p': 0.05,
        '720p': 0.1,
        '1080p': 0.2,
        '4K': 0.5
    }

    # Energy consumption rates (in kWh) for different device types
    device_energy = {
        'low': 0.05,    # Low-end devices
        'medium': 0.1,  # Mid-range devices
        'high': 0.2     # High-end devices
    }

    # Energy consumption rates (in kWh) based on network speed
    network_energy = {
        'slow': 0.01,
        'average': 0.05,
        'fast': 0.1
    }

    # Get energy consumption for the given resolution
    energy_per_minute = resolution_energy.get(resolution, 0.1)  # Default to 0.1 if resolution not found

    # Determine device energy consumption based on device architecture
    device_architecture = device_specs.get('architecture', '').lower()
    if 'high' in device_architecture:
        device_energy_consumption = device_energy['high']
    elif 'medium' in device_architecture:
        device_energy_consumption = device_energy['medium']
    else:
        device_energy_consumption = device_energy['low']

    # Determine network energy consumption based on connection speed
    network_energy_consumption = network_energy.get(connection_speed, network_energy['average'])

    # Calculate total energy consumption
    total_energy_consumption = (energy_per_minute + device_energy_consumption + network_energy_consumption) * duration

    # Carbon emission factor (in kg CO2 per kWh)
    carbon_emission_factor = 0.5

    # Calculate carbon emissions
    carbon_emissions = total_energy_consumption * carbon_emission_factor

    return {
        'energy_consumption': total_energy_consumption,
        'carbon_emissions': carbon_emissions
    }

def generate_recommendations(user_id, carbon_footprint):
    """
    Generate recommendations based on the carbon footprint of a video call.
    """
    recommendations = []

    # Generate recommendations based on carbon emissions and energy consumption
    if carbon_footprint.carbon_emissions > 10:  # Example threshold
        recommendations.append(Recommendation(user_id=user_id, recommendation_text="Consider reducing the video resolution to 720p or lower."))
    if carbon_footprint.energy_consumption > 5:  # Example threshold
        recommendations.append(Recommendation(user_id=user_id, recommendation_text="Try to limit the duration of your video calls."))

    # Save recommendations to the database
    for rec in recommendations:
        db.session.add(rec)
    db.session.commit()

    return recommendations

def get_internet_speed():
    """Get the current internet speed using multiple methods."""
    try:
        # Try speedtest-cli first
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        return {'download_speed': download_speed, 'upload_speed': upload_speed}
    except speedtest.SpeedtestHTTPError as e:
        logging.warning(f"Speedtest HTTP error: {e}. Trying alternative method.")
    except Exception as e:
        logging.warning(f"Error with speedtest-cli: {e}. Trying alternative method.")

    # If speedtest-cli fails, try a simple download test
    try:
        url = "http://speedtest.ftp.otenet.gr/files/test1Mb.db"
        start_time = time.time()
        response = requests.get(url, timeout=10,stream=True)
        end_time = time.time()
        if response.status_code == 200:
            file_size = len(response.content) / 1_000_000  # Size in MB
            duration = end_time - start_time
            download_speed = (file_size * 8) / duration  # Convert to Mbps
            return {'download_speed': download_speed, 'upload_speed': 0.0}
    except requests.RequestException as e:
        logging.warning(f"Error with alternative speed test: {e}")

    # If both methods fail, try a simple ping test
    try:
        host = "8.8.8.8"  # Google's public DNS server
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
        if result.returncode == 0:
            logging.info("Ping test successful. Internet connection is available.")
            return {'download_speed': 0.1, 'upload_speed': 0.1}  # Return minimal non-zero values
        else:
            logging.warning("Ping test failed. No internet connection detected.")
    except subprocess.SubprocessError as e:
        logging.warning(f"Error with ping test: {e}")

    # If all methods fail, return default values
    logging.warning("All internet connection tests failed. Returning default values.")
    return {'download_speed': 0.0, 'upload_speed': 0.0}

def get_video_resolution():
    """
    Get the current video resolution from the webcam.
    """
    try:
        cap = cv2.VideoCapture(0)  # Open the default camera
        if not cap.isOpened():
            return {"error": "Could not open webcam"}
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()  # Release the camera
        return {'resolution': f"{width}x{height}"}
    except Exception as e:
        logging.error(f"Error getting video resolution: {e}")
        return {"error": "Could not retrieve video resolution"}

def get_device_specs():
    """
    Get device specifications.
    """
    return {
        'device': platform.node(),
        'os': platform.system(),
        'os_version': platform.version(),
        'processor': platform.processor(),
        'architecture': platform.architecture()[0]
    }