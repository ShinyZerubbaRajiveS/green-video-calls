from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
import os

# Initialize the database
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize the database with the app
    db.init_app(app)

    # Initialize Flask-Migrate
    migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'migrations')
    if os.path.exists(migrations_dir):
        migrate.init_app(app, db, directory=migrations_dir)
    else:
        logging.error(f"Migrations directory not found: {migrations_dir}")

    with app.app_context():
        # Import and register routes as a blueprint
        from app.routes import bp
        app.register_blueprint(bp)

        # Gather initial data for real-time implementation
        from app.utils import get_device_specs, get_internet_speed, get_video_resolution
        
        try:
            device_specs = get_device_specs()
            internet_speed = get_internet_speed()
            video_resolution = get_video_resolution()

            logging.info("Initial Device Specifications: %s", device_specs)
            logging.info("Initial Internet Speed: %s", internet_speed)
            logging.info("Initial Video Resolution: %s", video_resolution)
        except Exception as e:
            logging.error("Error gathering initial data: %s", str(e))

    return app