# from flask import Blueprint, request, jsonify, render_template
# from app import db
# from app.models import VideoCall, CarbonFootprint, Recommendation, User
# from app.utils import (
#     calculate_carbon_footprint,
#     get_internet_speed,
#     get_video_resolution,
#     get_device_specs
# )

# bp = Blueprint('routes', __name__)

# @bp.route('/')
# def index():
#     """Render the index page with the form for submitting call data."""
#     return render_template('index.html')

# @bp.route('/add_call', methods=['POST'])
# def add_call():
#     """Handle the submission of call data and redirect to the meeting link."""
#     try:
#         data = request.get_json()  # Expecting JSON data
#         if not data:
#             return jsonify({"error": "No data provided"}), 400

#         # Check if required fields are present in the data
#         if 'user_id' not in data or 'meeting_link' not in data:
#             return jsonify({"error": "Missing required fields: user_id and meeting_link"}), 400

#         user_id = data['user_id']
#         meeting_link = data['meeting_link']

#         # Check if the user exists in the users table
#         user = db.session.query(User).filter_by(id=user_id).first()

#         if not user:
#             # If the user does not exist, create a new user
#             username = data.get('username')
#             email = data.get('email')

#             # Check if all required fields for user creation are provided
#             if not username or not email:
#                 return jsonify({"error": "Missing required fields for user creation."}), 400

#             # Create a new user
#             new_user = User(username=username, email=email)
#             db.session.add(new_user)
#             db.session.commit()  # Commit to save the user

#             user_id = new_user.id  # Update user_id to the new user's ID

#         # Automatically gather device specifications and internet speed
#         device_specs = get_device_specs()
#         internet_speed = get_internet_speed()
#         video_resolution = get_video_resolution()

#         # Create a new video call entry
#         new_call = VideoCall(
#             user_id=user_id,
#             duration=30,  # Example duration, replace with actual logic
#             resolution=video_resolution['resolution'],  # Use auto-detected resolution
#             connection_speed=internet_speed['download_speed'],  # Use auto-detected speed
#             device_specs=device_specs  # Use auto-detected device specs
#         )
#         db.session.add(new_call)
#         db.session.commit()

#         # Calculate carbon footprint based on video quality
#         emissions = calculate_carbon_footprint(
#             new_call.duration,
#             new_call.resolution,
#             new_call.connection_speed,
#             new_call.device_specs
#         )

#         # Create a new carbon footprint entry
#         new_footprint = CarbonFootprint(
#             call_id=new_call.id,
#             energy_consumption=emissions['energy_consumption'],
#             carbon_emissions=emissions['carbon_emissions']
#         )
#         db.session.add(new_footprint)
#         db.session.commit()

#         # Generate recommendations
#         recommendation_text = "Try to limit the duration of your video calls."  # Example recommendation text
#         recommendation = Recommendation(
#             user_id=user_id,
#             recommendation_text=recommendation_text
#         )
#         db.session.add(recommendation)
#         db.session.commit()

#         # Return the meeting link for redirection, call data, and carbon footprint information
#         return jsonify({
#             'redirect_url': meeting_link,  # Open meeting link in a new tab
#             'call': new_call.to_dict(),
#             'carbon_footprint': new_footprint.to_dict(),  # Ensure using to_dict() method
#             'recommendation': recommendation.to_dict()  # Return recommendation data
#         }), 201  # Return a 201 Created status

#     except Exception as e:
#         print("Error in add_call:", e)  # Log the error for debugging
#         return jsonify({"error": "An error occurred while processing the request."}), 500
from flask import Blueprint, request, jsonify, render_template
from app.models import db, VideoCall, CarbonFootprint
from app.utils import calculate_carbon_footprint, generate_recommendations, get_internet_speed

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Render the index page with the form for submitting call data."""
    return render_template('index.html')

@bp.route('/add_call', methods=['POST'])
def add_call():
    """Add a new video call and calculate initial carbon footprint."""
    data = request.get_json()

    # Extract parameters from request
    user_id = data.get('user_id')
    meeting_link = data.get('meeting_link')
    username = data.get('username')
    email = data.get('email')

    # Get internet speed dynamically using the utility function
    internet_speed = get_internet_speed()
    connection_speed = 'fast' if internet_speed['download_speed'] > 20 else 'slow'  # Example logic
    
    # Video resolution and device specs could be gathered from the request or other methods
    resolution = data.get('resolution', '1080p')  # Default to '1080p'
    device_specs = data.get('device_specs', 'high-end')  # Default to 'high-end'

    # Create a new video call entry
    call = VideoCall(user_id=user_id, meeting_link=meeting_link, username=username, email=email, duration=0)
    db.session.add(call)
    db.session.commit()

    # Initial carbon footprint calculation
    emissions = calculate_carbon_footprint(
        duration=call.duration,
        resolution=resolution,
        connection_speed=connection_speed,
        device_specs=device_specs
    )

    # Create carbon footprint entry
    footprint = CarbonFootprint(
        call_id=call.id,
        energy_consumption=emissions['energy_consumption'],
        carbon_emissions=emissions['carbon_emissions']
    )
    db.session.add(footprint)
    db.session.commit()

    # Generate recommendations (optional)
    recommendation_text = generate_recommendations(user_id, footprint)

    # Return response with call info and redirect URL
    return jsonify({
        'call': {
            'id': call.id,
            'meeting_link': meeting_link
        },
        'redirect_url': meeting_link
    })

@bp.route('/update_call/<int:call_id>', methods=['GET'])
def update_call(call_id):
    """Update the call duration and recalculate the carbon footprint."""
    try:
        # Get the new duration from the query parameter
        duration = request.args.get('duration', type=int)

        # Find the call and related carbon footprint entry
        call = db.session.query(VideoCall).filter_by(id=call_id).first()
        if not call:
            return jsonify({"error": "Call not found"}), 404

        # Get internet speed dynamically using the utility function
        internet_speed = get_internet_speed()
        connection_speed = 'fast' if internet_speed['download_speed'] > 20 else 'slow'  # Example logic

        # Update the call duration
        call.duration = duration
        db.session.commit()

        # Recalculate carbon footprint
        emissions = calculate_carbon_footprint(
            call.duration,
            call.resolution,  # Assuming resolution is stored in the `VideoCall` model
            connection_speed,
            call.device_specs  # Assuming device specs are stored in the `VideoCall` model
        )

        # Update the carbon footprint entry
        footprint = db.session.query(CarbonFootprint).filter_by(call_id=call.id).first()
        if not footprint:
            return jsonify({"error": "Carbon footprint not found"}), 404

        footprint.energy_consumption = emissions['energy_consumption']
        footprint.carbon_emissions = emissions['carbon_emissions']
        db.session.commit()

        # Generate recommendations (optional, or use existing ones)
        recommendation_text = generate_recommendations(call.user_id, footprint)

        return jsonify({
            'carbon_footprint': footprint.to_dict(),
            'recommendation': {
                'recommendation_text': recommendation_text
            }
        })

    except Exception as e:
        print("Error in update_call:", e)
        return jsonify({"error": "An error occurred while updating the call."}), 500

