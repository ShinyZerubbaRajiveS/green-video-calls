from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import platform
import speedtest
import cv2

# Initialize the database and migration objects
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database and migration with the app
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Import and register routes as a blueprint
        from app.routes import bp
        app.register_blueprint(bp)

        # Gather initial data for real-time implementation
        gather_initial_data()

    return app

def gather_initial_data():
    """Function to gather initial data such as device specs, internet speed, and video resolution."""
    try:
        device_specs = get_device_specs()
        internet_speed = get_internet_speed()
        video_resolution = get_video_resolution()

        print("Initial Device Specifications:", device_specs)
        print("Initial Internet Speed:", internet_speed)
        print("Initial Video Resolution:", video_resolution)
    except Exception as e:
        print("Error gathering initial data:", e)

def get_device_specs():
    """Get device specifications."""
    return {
        'device_name': platform.node(),
        'operating_system': platform.system(),
        'os_version': platform.version(),
        'processor': platform.processor(),
        'architecture': platform.architecture()[0]
    }

def get_internet_speed():
    """Get the current internet speed."""
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
    """Get the current video resolution from the webcam."""
    cap = cv2.VideoCapture(0)  # Open the default camera
    if not cap.isOpened():
        return {"error": "Could not open webcam"}
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()  # Release the camera
    return {
        'resolution': f"{width}x{height}"
    }