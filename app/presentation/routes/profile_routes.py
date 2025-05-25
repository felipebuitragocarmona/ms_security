from flask import Blueprint, request, jsonify
from app.business.controllers.profile_controller import ProfileController

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/', methods=['GET'])
def get_all_profiles():
    """Get all profiles"""
    result, status_code = ProfileController.get_all()
    return jsonify(result), status_code

@profile_bp.route('/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    """Get a specific profile by ID"""
    result, status_code = ProfileController.get_by_id(profile_id)
    return jsonify(result), status_code

@profile_bp.route('/user/<int:user_id>', methods=['GET'])
def get_profile_by_user(user_id):
    """Get a profile by user ID"""
    result, status_code = ProfileController.get_by_user_id(user_id)
    return jsonify(result), status_code

@profile_bp.route('/user/<int:user_id>', methods=['POST'])
def create_profile(user_id):
    """Create a new profile for a user"""
    data = request.form.to_dict()
    photo = request.files.get('photo')
    result, status_code = ProfileController.create(user_id, data, photo)
    return jsonify(result), status_code

@profile_bp.route('/<int:profile_id>', methods=['PUT'])
def update_profile(profile_id):
    """Update a profile"""
    data = request.form.to_dict()
    photo = request.files.get('photo')
    result, status_code = ProfileController.update(profile_id, data, photo)
    return jsonify(result), status_code

@profile_bp.route('/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    """Delete a profile"""
    result, status_code = ProfileController.delete(profile_id)
    return jsonify(result), status_code