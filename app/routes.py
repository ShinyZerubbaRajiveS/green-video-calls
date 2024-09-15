from flask import Blueprint, request, jsonify, render_template
from app.models import db, VideoCall, CarbonFootprint, Recommendation
from app.utils import calculate_carbon_footprint, generate_recommendations, get_internet_speed
import json
import logging

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Render the index page with the form for submitting call data."""
    return render_template('index.html')

@bp.route('/add_call', methods=['POST'])
def add_call():
    """Add a new video call and calculate initial carbon footprint."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_id = data.get('user_id')
        meeting_link = data.get('meeting_link')
        username = data.get('username')
        email = data.get('email')
        resolution = data.get('resolution', '1080p')
        device_specs = data.get('device_specs', {'device': 'high-end'})

        if not user_id or not meeting_link:
            return jsonify({"error": "Missing required fields: user_id and meeting_link"}), 400

        internet_speed = get_internet_speed()
        download_speed = float(internet_speed.get('download_speed', 0))
        connection_speed = 'fast' if download_speed > 20 else 'slow'

        # Create a new VideoCall object
        call = VideoCall(
            user_id=user_id,
            meeting_link=meeting_link,
            username=username,
            email=email,
            duration=0,  # Default duration, will be updated later
            resolution=resolution,
            connection_speed=connection_speed,
            device_specs=json.dumps(device_specs)  # Store as JSON string
        )
        db.session.add(call)
        db.session.commit()

        # Calculate the carbon footprint using the utility function
        emissions = calculate_carbon_footprint(
            duration=call.duration,
            resolution=resolution,
            connection_speed=connection_speed,
            device_specs=device_specs
        )

        # Create a new CarbonFootprint record
        footprint = CarbonFootprint(
            call_id=call.id,
            energy_consumption=emissions['energy_consumption'],
            carbon_emissions=emissions['carbon_emissions']
        )
        db.session.add(footprint)
        db.session.commit()

        # Generate recommendations based on the user and footprint
        recommendations = generate_recommendations(user_id, footprint)

        return jsonify({
            'call': call.to_dict(),
            'redirect_url': meeting_link,
            'carbon_footprint': footprint.to_dict(),
            'recommendations': [rec.to_dict() for rec in recommendations]
        }), 201

    except ValueError as ve:
        logging.error("ValueError in add_call: %s", str(ve))
        return jsonify({"error": f"Invalid input: {str(ve)}"}), 400

    except json.JSONDecodeError as json_err:
        logging.error("JSONDecodeError in add_call: %s", str(json_err))
        return jsonify({"error": "Invalid JSON format"}), 400

    except Exception as e:
        logging.error("Error in add_call: %s", str(e))
        return jsonify({"error": f"An error occurred while processing the request: {str(e)}"}), 500

@bp.route('/update_call/<int:call_id>', methods=['GET'])
def update_call(call_id):
    """Update call duration and calculate new carbon footprint."""
    try:
        duration = request.args.get('duration', type=int)
        if duration is None:
            return jsonify({'error': 'Duration not provided'}), 400
        
        # Fetch the call from the database
        call = VideoCall.query.get(call_id)
        if not call:
            return jsonify({'error': 'Call not found'}), 404

        # Update the duration
        call.duration = duration
        db.session.commit()

        # Calculate the updated carbon footprint
        emissions = calculate_carbon_footprint(
            duration=call.duration,
            resolution=call.resolution,
            connection_speed=call.connection_speed,
            device_specs=json.loads(call.device_specs)  # Convert JSON string back to dictionary
        )

        # Update the CarbonFootprint record
        footprint = CarbonFootprint.query.filter_by(call_id=call_id).first()
        if not footprint:
            footprint = CarbonFootprint(
                call_id=call.id,
                energy_consumption=emissions['energy_consumption'],
                carbon_emissions=emissions['carbon_emissions']
            )
            db.session.add(footprint)
        else:
            footprint.energy_consumption = emissions['energy_consumption']
            footprint.carbon_emissions = emissions['carbon_emissions']

        db.session.commit()

        # Generate recommendations based on the user and updated footprint
        recommendations = generate_recommendations(call.user_id, footprint)

        return jsonify({
            'message': 'Call updated successfully',
            'carbon_footprint': footprint.to_dict(),
            'recommendations': [rec.to_dict() for rec in recommendations]
        }), 200

    except Exception as e:
        logging.error("Error in update_call: %s", str(e))
        return jsonify({"error": f"An error occurred while processing the request: {str(e)}"}), 500