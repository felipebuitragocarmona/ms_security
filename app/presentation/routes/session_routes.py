from flask import Blueprint, request, jsonify
from app.business.controllers.session_controller import SessionController

session_bp = Blueprint('session_bp', __name__)

@session_bp.route('/', methods=['GET'])
def get_all_sessions():
    """Get all sessions"""
    result, status_code = SessionController.get_all()
    return jsonify(result), status_code

@session_bp.route('/<string:session_id>', methods=['GET'])
def get_session(session_id):
    """Get a specific session by ID"""
    result, status_code = SessionController.get_by_id(session_id)
    return jsonify(result), status_code

@session_bp.route('/user/<int:user_id>', methods=['GET'])
def get_sessions_by_user(user_id):
    """Get all sessions for a specific user"""
    result, status_code = SessionController.get_by_user_id(user_id)
    return jsonify(result), status_code

@session_bp.route('/user/<int:user_id>', methods=['POST'])
def create_session(user_id):
    """Create a new session for a user"""
    data = request.json
    result, status_code = SessionController.create(user_id, data)
    return jsonify(result), status_code

@session_bp.route('/<string:session_id>', methods=['PUT'])
def update_session(session_id):
    """Update a session"""
    data = request.json
    result, status_code = SessionController.update(session_id, data)
    return jsonify(result), status_code

@session_bp.route('/<string:session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a session"""
    result, status_code = SessionController.delete(session_id)
    return jsonify(result), status_code