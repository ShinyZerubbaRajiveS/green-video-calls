# from app.models import Recommendation
# from app import db
# import platform
# import speedtest
# import cv2

# def calculate_carbon_footprint(duration, resolution, connection_speed, device_specs):
#     # Example energy consumption rates (in kWh)
#     resolution_energy = {
#         '480p': 0.05,
#         '720p': 0.1,
#         '1080p': 0.2,
#         '4K': 0.5
#     }

#     # Example device energy consumption rates (in kWh)
#     device_energy = {
#         'low': 0.05,    # Low-end devices
#         'medium': 0.1,  # Mid-range devices
#         'high': 0.2     # High-end devices
#     }

#     # Example network energy consumption rates (in kWh)
#     network_energy = {
#         'slow': 0.01,
#         'average': 0.05,
#         'fast': 0.1
#     }

#     # Determine energy consumption based on resolution
#     energy_per_minute = resolution_energy.get(resolution, 0.1)  # Default to 0.1 if resolution not found

#     # Determine device energy consumption based on architecture
#     if 'high' in device_specs.get('architecture', '').lower():
#         device_energy_consumption = device_energy['high']
#     elif 'medium' in device_specs.get('architecture', '').lower():
#         device_energy_consumption = device_energy['medium']
#     else:
#         device_energy_consumption = device_energy['low']

#     # Determine network energy consumption based on connection speed
#     if connection_speed > 100:
#         network_energy_consumption = network_energy['fast']
#     elif connection_speed > 10:
#         network_energy_consumption = network_energy['average']
#     else:
#         network_energy_consumption = network_energy['slow']

#     # Calculate total energy consumption
#     total_energy_consumption = (energy_per_minute + device_energy_consumption + network_energy_consumption) * duration

#     # Example carbon emission factor (in kg CO2 per kWh)
#     carbon_emission_factor = 0.5

#     # Calculate carbon emissions
#     carbon_emissions = total_energy_consumption * carbon_emission_factor

#     return {
#         'energy_consumption': total_energy_consumption,
#         'carbon_emissions': carbon_emissions
#     }

# def generate_recommendations(user_id, carbon_footprint):
#     recommendations = []

#     if carbon_footprint['carbon_emissions'] > 10:  # Example threshold
#         recommendations.append("Consider reducing the video resolution to 720p or lower.")
#     if carbon_footprint['energy_consumption'] > 5:  # Example threshold
#         recommendations.append("Try to limit the duration of your video calls.")
#     if 'high' in carbon_footprint.get('device_specs', {}).get('architecture', '').lower():
#         recommendations.append("Consider using a more energy-efficient device.")

#     # Save recommendations to the database
#     for rec in recommendations:
#         new_recommendation = Recommendation(user_id=user_id, recommendation_text=rec)
#         db.session.add(new_recommendation)
#     db.session.commit()

#     return recommendations

# def get_internet_speed():
#     """Get the current internet speed."""
#     try:
#         st = speedtest.Speedtest()
#         st.get_best_server()  # Optional: Find the best server
#         download_speed = st.download() / 1_000_000  # Convert to Mbps
#         upload_speed = st.upload() / 1_000_000  # Convert to Mbps
#         return {
#             'download_speed': download_speed,
#             'upload_speed': upload_speed
#         }
#     except Exception as e:
#         print("Error getting internet speed:", e)
#         return {'download_speed': 0, 'upload_speed': 0}  # Return default values on error

# def get_video_resolution():
#     """Get the current video resolution from the webcam."""
#     try:
#         cap = cv2.VideoCapture(0)  # Open the default camera
#         if not cap.isOpened():
#             return {"error": "Could not open webcam"}
        
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         cap.release()  # Release the camera
#         return {
#             'resolution': f"{width}x{height}"
#         }
#     except Exception as e:
#         print("Error getting video resolution:", e)
#         return {"error": "Could not retrieve video resolution"}

# def get_device_specs():
#     """Get device specifications."""
#     return {
#         'device_name': platform.node(),
#         'operating_system': platform.system(),
#         'os_version': platform.version(),
#         'processor': platform.processor(),
#         'architecture': platform.architecture()[0]
#     }

from app.models import Recommendation
from app import db
import platform
import speedtest
import cv2

def calculate_carbon_footprint(duration, resolution, connection_speed, device_specs):
    """
    Calculate the carbon footprint based on call duration, video resolution, 
    connection speed, and device specifications.

    Args:
        duration (int): Duration of the call in minutes.
        resolution (str): Video resolution (e.g., '480p', '720p').
        connection_speed (int): Internet connection speed in Mbps.
        device_specs (dict): Specifications of the device.

    Returns:
        dict: A dictionary containing total energy consumption and carbon emissions.
    """
    # Example energy consumption rates (in kWh)
    resolution_energy = {
        '480p': 0.05,
        '720p': 0.1,
        '1080p': 0.2,
        '4K': 0.5
    }

    # Example device energy consumption rates (in kWh)
    device_energy = {
        'low': 0.05,    # Low-end devices
        'medium': 0.1,  # Mid-range devices
        'high': 0.2     # High-end devices
    }

    # Example network energy consumption rates (in kWh)
    network_energy = {
        'slow': 0.01,
        'average': 0.05,
        'fast': 0.1
    }

    # Determine energy consumption based on resolution
    energy_per_minute = resolution_energy.get(resolution, 0.1)  # Default to 0.1 if resolution not found

    # Determine device energy consumption based on architecture
    if 'high' in device_specs.get('architecture', '').lower():
        device_energy_consumption = device_energy['high']
    elif 'medium' in device_specs.get('architecture', '').lower():
        device_energy_consumption = device_energy['medium']
    else:
        device_energy_consumption = device_energy['low']

    # Determine network energy consumption based on connection speed
    if connection_speed > 100:
        network_energy_consumption = network_energy['fast']
    elif connection_speed > 10:
        network_energy_consumption = network_energy['average']
    else:
        network_energy_consumption = network_energy['slow']

    # Calculate total energy consumption
    total_energy_consumption = (energy_per_minute + device_energy_consumption + network_energy_consumption) * duration

    # Example carbon emission factor (in kg CO2 per kWh)
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

    Args:
        user_id (int): The ID of the user.
        carbon_footprint (dict): The carbon footprint data.

    Returns:
        list: A list of recommendations.
    """
    recommendations = []

    if 'carbon_emissions' in carbon_footprint and carbon_footprint['carbon_emissions'] > 10:  # Example threshold
        recommendations.append("Consider reducing the video resolution to 720p or lower.")
    if 'energy_consumption' in carbon_footprint and carbon_footprint['energy_consumption'] > 5:  # Example threshold
        recommendations.append("Try to limit the duration of your video calls.")
    if 'device_specs' in carbon_footprint and 'architecture' in carbon_footprint['device_specs']:
        if 'high' in carbon_footprint['device_specs']['architecture'].lower():
            recommendations.append("Consider using a more energy-efficient device.")

    # Save recommendations to the database
    for rec in recommendations:
        new_recommendation = Recommendation(user_id=user_id, recommendation_text=rec)
        db.session.add(new_recommendation)
    db.session.commit()

    return recommendations

def get_internet_speed():
    """
    Get the current internet speed.

    Returns:
        dict: A dictionary containing download and upload speeds in Mbps.
    """
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  # Optional: Find the best server
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        return {
            'download_speed': download_speed,
            'upload_speed': upload_speed
        }
    except Exception as e:
        print("Error getting internet speed:", e)
        return {'download_speed': 0, 'upload_speed': 0}  # Return default values on error

def get_video_resolution():
    """
    Get the current video resolution from the webcam.

    Returns:
        dict: A dictionary containing the video resolution or an error message.
    """
    try:
        cap = cv2.VideoCapture(0)  # Open the default camera
        if not cap.isOpened():
            return {"error": "Could not open webcam"}
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()  # Release the camera
        return {
            'resolution': f"{width}x{height}"
        }
    except Exception as e:
        print("Error getting video resolution:", e)
        return {"error": "Could not retrieve video resolution"}

def get_device_specs():
    """
    Get device specifications.

    Returns:
        dict: A dictionary containing device specifications.
    """
    return {
        'device_name': platform.node(),
        'operating_system': platform.system(),
        'os_version': platform.version(),
        'processor': platform.processor(),
        'architecture': platform.architecture()[0]
    }