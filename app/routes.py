from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import User, VideoCall, CarbonFootprint, Recommendation
from app.utils import calculate_carbon_footprint, generate_recommendations
import json
import logging

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/add_call', methods=['POST'])
def add_call():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'meeting_link']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Create or get user
        user = User.query.get(data['user_id'])
        if not user:
            if not all(field in data for field in ['username', 'email']):
                return jsonify({"error": "New user requires username and email"}), 400
            user = User(
                id=data['user_id'],
                username=data['username'],
                email=data['email']
            )
            db.session.add(user)

        # Create video call
        call = VideoCall(
            user_id=user.id,
            meeting_link=data['meeting_link'],
            duration=0,
            resolution=data.get('resolution', '720p'),
            connection_speed=data.get('connection_speed', 'average'),
            device_specs=data.get('device_specs', {'type': 'unknown'})
        )
        db.session.add(call)
        db.session.commit()

        # Calculate initial footprint
        footprint_data = calculate_carbon_footprint(
            duration=0,
            resolution=call.resolution,
            connection_speed=call.connection_speed,
            device_specs=call.device_specs
        )

        footprint = CarbonFootprint(
            call_id=call.id,
            energy_consumption=footprint_data['energy_consumption'],
            carbon_emissions=footprint_data['carbon_emissions']
        )
        db.session.add(footprint)
        
        # Generate recommendations
        recommendations = generate_recommendations(user.id, footprint)
        
        db.session.commit()

        return jsonify({
            "status": "success",
            "call_id": call.id,
            "redirect_url": call.meeting_link,
            "carbon_footprint": footprint_data,
            "recommendations": [r.recommendation_text for r in recommendations]
        }), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in add_call: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/update_call/<int:call_id>', methods=['GET'])
def update_call(call_id):
    try:
        duration = request.args.get('duration', type=int)
        if not duration:
            return jsonify({"error": "Duration parameter required"}), 400

        call = VideoCall.query.get_or_404(call_id)
        call.duration = duration
        db.session.commit()

        footprint_data = calculate_carbon_footprint(
            duration=duration,
            resolution=call.resolution,
            connection_speed=call.connection_speed,
            device_specs=call.device_specs
        )

        footprint = CarbonFootprint.query.filter_by(call_id=call_id).first()
        if not footprint:
            footprint = CarbonFootprint(call_id=call_id)
            db.session.add(footprint)
        
        footprint.energy_consumption = footprint_data['energy_consumption']
        footprint.carbon_emissions = footprint_data['carbon_emissions']
        
        recommendations = generate_recommendations(call.user_id, footprint)
        db.session.commit()

        return jsonify({
            "status": "success",
            "carbon_footprint": footprint_data,
            "recommendations": [r.recommendation_text for r in recommendations]
        }), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in update_call: {str(e)}")
        return jsonify({"error": str(e)}), 500